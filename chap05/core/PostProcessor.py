from core.Geometry import Geometry
from core.RendererTarget import RenderTarget
from core.Scene import Scene
from core.Camera import Camera
from core.Mesh import Mesh

class PostProcessor(object):
    """Add effects which can be stacked over each other"""

    def __init__(self, renderer, scene, camera, finalRenderTarget=None):
        super(PostProcessor, self).__init__()

        self.renderer = renderer
        self.sceneList = [scene]
        self.cameraList = [camera]
        self.renderTargetList = [finalRenderTarget]
        self.finalRenderTarget = finalRenderTarget

        # generate a rectangle plane geometry to be used as a virtual screen (think of each effect as a layer)

        self.rectangleGeo = Geometry()
        p0, p1, p2, p3 = [-1,-1], [1,-1], [-1,1], [1,1]
        t0, t1, t2, t3 = [0,0], [1,0], [0,1], [1,1]
        positionData = [p0,p1,p3, p0,p3,p2]
        uvData = [t0,t1,t3, t0,t3,t2]

        self.rectangleGeo.addAttribute("vec2", "vertexPosition", positionData)
        self.rectangleGeo.addAttribute("vec2", "vertexUV", uvData)
        self.rectangleGeo.countVertices()

    def addEffect(self, effect):
        postScene = Scene()
        renderTarget = RenderTarget(resolution=self.renderer.windowSize)

        orthogonalCamera = Camera()
        orthogonalCamera.setOrthographic()
        
        effect.uniforms["texture"].data[0] = renderTarget.texture.textureReference
        mesh = Mesh(self.rectangleGeo, effect)
        postScene.add(mesh)

        self.renderTargetList[-1] = renderTarget
        self.sceneList.append(postScene)
        self.cameraList.append(orthogonalCamera)

        self.renderTargetList.append(self.finalRenderTarget)

    def render(self):

        for n in range(len(self.sceneList)):
            scene = self.sceneList[n]
            camera = self.cameraList[n]
            target = self.renderTargetList[n]

            self.renderer.render(scene, camera, renderTarget=target)
        
