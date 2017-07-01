/*
 *	Copyright (C) 2012 Visualization & Graphics Lab (VGL), Indian Institute of Science
 *
 *	This file is part of Recon, a library to compute Reeb graphs.
 *
 *	Recon is free software: you can redistribute it and/or modify
 *	it under the terms of the GNU Lesser General Public License as published by
 *	the Free Software Foundation, either version 3 of the License, or
 *	(at your option) any later version.
 *
 *	Recon is distributed in the hope that it will be useful,
 *	but WITHOUT ANY WARRANTY; without even the implied warranty of
 *	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *	GNU Lesser General Public License for more details.
 *
 *	You should have received a copy of the GNU Lesser General Public License
 *	along with Recon.  If not, see <http://www.gnu.org/licenses/>.
 *
 *	Author(s):	Harish Doraiswamy
 *	Version	 :	1.0
 *
 *	Modified by : -- 
 *	Date : --
 *	Changes  : --
 */
package vgl.iisc.reebgraph.ui;

import java.util.Iterator;

import vgl.iisc.reebgraph.ui.BranchDecomposition.Branch;
import vgl.iisc.utils.Triple;


public class ReebGraphLayout {
	
	public class Point {
		public Triple<Float> loc = new Triple<Float>(0f,0f,0f);
		
	    @Override
	    public String toString() {
	        return "(" + loc.x +", "+ loc.y + ", " + loc.z+")";
	    }
	}
	
	public class BranchLocation {
		public int id;
		float angle;
		int level;
		public float x,z;
	}
	
	public Point [] nodes;
	public BranchLocation [] branches;
	int noNodes;
	int noBranches;
	int [] leafCount;
	float [] startAngle;
	BranchDecomposition bd;
	ReebGraphData data;
	int noLeaves;
	int maxLevel;
	int lastIndex;
	float [] r;
	
	public void layoutBranches(BranchDecomposition bd, ReebGraphData data, int lastIncludedBranch) {
		this.bd = bd;
		this.data = data;
		lastIndex = lastIncludedBranch;
		maxLevel = 0;
		
		noNodes = data.noNodes;
		noBranches = bd.branches.size();
		
		nodes = new Point[noNodes];
		leafCount = new int[noBranches];
		startAngle = new float[noBranches];
		branches = new BranchLocation[noBranches];
		for(int i = 0;i < noBranches;i ++) {
			branches[i] = new BranchLocation();
		}
		noLeaves = countLeaves(bd.branches.get(0), 0);
		
		r = new float[maxLevel + 1];
		r[0] = 0;
		if(maxLevel > 0) {
			r[1] = 1;
		}
		for(int i = 2;i <= maxLevel;i ++) {
			r[i] = r[i - 1] * rootTwo;
		}
		branches[0].angle = (float) (2 * Math.PI);
		startAngle[0] = 0;
		assignAngles(bd.branches.get(0));
		assignLocations();
	}
	
	private int countLeaves(Branch br, int level) {
		branches[br.id] = new BranchLocation();
		branches[br.id].level = level;
		if(br.children.size() > 0) {
			for(Iterator<Branch> it = br.children.iterator();it.hasNext();) {
				Branch ch = it.next();
				if(ch.id <= lastIndex) {
					leafCount[br.id] += countLeaves(ch, level + 1);
				}
			}
			if(leafCount[br.id] == 0) {
				leafCount[br.id] = 1;
				maxLevel = Math.max(level, maxLevel);
			}
			return leafCount[br.id];
		} else {
			leafCount[br.id] = 1;
			maxLevel = Math.max(level, maxLevel);
			return 1;
		}
	}
	static final float rootTwo = (float) Math.sqrt(2);
	
	void assignAngles(Branch br) {
		int i = br.id;
		float totAng = branches[i].angle; 
		int totCh = leafCount[i];
		float add = startAngle[br.id];
		for(Iterator<Branch> it = br.children.iterator();it.hasNext();) {
			Branch ch = it.next();
			if(ch.id > lastIndex) {
				continue;
			}
			branches[ch.id].angle = totAng * leafCount[ch.id];
			branches[ch.id].angle /= totCh;
			if(i == 0) {
				if(branches[ch.id].angle > Math.PI / 2) {
					branches[ch.id].angle = (float) (Math.PI / 2);
				}
			}
			startAngle[ch.id] = add;
			add += branches[ch.id].angle;
			float ang = startAngle[ch.id] + branches[ch.id].angle/2;
			float rad = r[branches[ch.id].level];
			branches[ch.id].x = (float) (rad * Math.sin(ang)); 
			branches[ch.id].z = (float) (rad * Math.cos(ang));
			assignAngles(ch);
		}
	}
	
	void assignLocations() {
		float maxFn = bd.branches.get(0).fn;
		float minFn = data.nodes[0].fn;
		float ratio;
		float valOfOne = 2;
		if(r.length > 2) {
			valOfOne = r[r.length - 1];
		}
		ratio = 2 * valOfOne / maxFn;
		for(int i = 0;i < noNodes;i ++) {
			nodes[i] = new Point();
			nodes[i].loc.y = (data.nodes[i].fn - minFn) * ratio - valOfOne;
			int bid = bd.nodeBranch[i];
			if(bid > lastIndex) {
				continue;
			}
			nodes[i].loc.x = branches[bid].x;
			nodes[i].loc.z = branches[bid].z;
		}
		extent = valOfOne * 2;
	}
	public float extent;
	
	public static void main(String [] args) {
		String file = "/home/sushmitha/workspace/recon/bunny.rg";
		ReebGraphData data = new ReebGraphData();
		data.readReebGraph(file);
		BranchDecomposition bd = new BranchDecomposition(data, true);
		bd.printBranches();
		ReebGraphLayout layout = new ReebGraphLayout();
		layout.layoutBranches(bd, data, bd.branches.size() - 1);
		for(int i = 0; i < data.noNodes; i++){
			System.out.println(i + " " + data.nodes[i].v + " " + data.nodes[i].fn + " " + data.nodes[i].type + " " + layout.nodes[i].toString());
		}
		
		System.out.println("Done");
	}
}
