# Demo script to show how to use tenon

# Define global variables
rootdir = '~/Dropbox/workspace/graphics_for_vision/tenon'
tenonpath = '~/Dropbox/workspace/graphics_for_vision/tenon/code'
pwd = '/home/qiuwch/Dropbox/workspace/graphics_for_vision/tenon/code/examples/demo_lsp'
import sys, os
sys.path.append(os.path.expanduser(tenonpath))
import tenon
sys.path.append(pwd)
import lsppose


def main():
    lsppose_ = lsppose.Util()
    lsppose_.rootdir = rootdir

    import tenon.logging as L
    outputdir = '//../cache/lsp_synthesized'
    L.setLevel(tenon.logging.INFO)
    L.info('Switch logging level to INFO')
    tenon.render.write('init.png')

    camera = tenon.obj.get('Camera') # Unused in this demo
    scene = lsppose_.setup_scene()

    for i in range(1, 2001):
        lsppose_.update_scene(scene, i)

        imgfilename = os.path.join(outputdir, 'imgs/%04d.png' % i)
        tenon.render.write(imgfilename)

        depth_filename = os.path.join(outputdir, 'depth/%04d.png' % i)
        tenon.render.DepthMode.enable()
        tenon.render.write(depth_filename)
        tenon.render.DepthMode.disable()

        paint_filename = os.path.join(outputdir, 'parts/%04d.png' % i)
        tenon.render.PaintMode.enable(tenon.obj.get('Suzanne'))
        tenon.render.write(paint_filename)

        # Also save the joint annotation and part annotation
        joint_filename = os.path.join(outputdir, 'joints/%04d.csv' % i)
        joints = lsppose.JointInfo.export()
        lsppose.JointInfo.serializeJointInfo(joint_filename, joints)


if __name__ == '__main__':
    # Avoid execution during module import
    if not tenon.inblender():
        scenefile = os.path.join(rootdir, 'data/mocap_demo_scene.blend')
        tenon.run(__file__, scenefile)
    else:
        main()
