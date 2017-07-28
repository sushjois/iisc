#### import the simple module from the paraview
from paraview.simple import *
import os
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

file_name = 'adhitya.vtp'
file_path = os.getcwd() + os.sep + file_name
tv_98graphvisualvtp = XMLPolyDataReader(FileName=[file_path])

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [909, 548]

# show data in view
tv_98graphvisualvtpDisplay = Show(tv_98graphvisualvtp, renderView1)
# trace defaults for the display properties.
tv_98graphvisualvtpDisplay.Representation = 'Surface'

# reset view to fit data
renderView1.ResetCamera()

# create a new 'TTK SphereFromPoint'
tTKSphereFromPoint1 = TTKSphereFromPoint(Input=tv_98graphvisualvtp)

# Properties modified on tTKSphereFromPoint1
tTKSphereFromPoint1.Radius = 0.15

# show data in view
tTKSphereFromPoint1Display = Show(tTKSphereFromPoint1, renderView1)
# trace defaults for the display properties.
tTKSphereFromPoint1Display.Representation = 'Surface'

# hide data in view
Hide(tv_98graphvisualvtp, renderView1)

# set active source
SetActiveSource(tv_98graphvisualvtp)

# show data in view
tv_98graphvisualvtpDisplay = Show(tv_98graphvisualvtp, renderView1)

# set active source
SetActiveSource(tTKSphereFromPoint1)

# set scalar coloring
ColorBy(tTKSphereFromPoint1Display, ('POINTS', 'NodeType'))

# rescale color and/or opacity maps used to include current data range
tTKSphereFromPoint1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
tTKSphereFromPoint1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'NodeType'
nodeTypeLUT = GetColorTransferFunction('NodeType')

# set active source
SetActiveSource(tv_98graphvisualvtp)

# create a new 'Tube'
tube1 = Tube(Input=tv_98graphvisualvtp)

# Properties modified on tube1
tube1.Vectors = [None, '']
tube1.Radius = 0.04

# show data in view
tube1Display = Show(tube1, renderView1)
# trace defaults for the display properties.
tube1Display.Representation = 'Surface'

# hide data in view
Hide(tv_98graphvisualvtp, renderView1)

# set active source
SetActiveSource(tv_98graphvisualvtp)

# show data in view
tv_98graphvisualvtpDisplay = Show(tv_98graphvisualvtp, renderView1)

# hide data in view
Hide(tv_98graphvisualvtp, renderView1)

# show data in view
tv_98graphvisualvtpDisplay = Show(tv_98graphvisualvtp, renderView1)

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [1.5966980755329132, -0.017842769622802734, 18.758492643983434]
renderView1.CameraFocalPoint = [1.5966980755329132, -0.017842769622802734, -0.1044418215751648]
renderView1.CameraParallelScale = 4.882086686207304

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
