import os
import subprocess
import sys
import argparse

DEBUG = False

if sys.platform.startswith('win'):
    PATH_DELIM = ';'
else:
    PATH_DELIM = ':'

# add this script's directory to PATH
os.environ['PATH'] += PATH_DELIM + os.path.dirname(os.path.abspath(__file__))

# add current directory to PATH
os.environ['PATH'] += PATH_DELIM + os.getcwd()

# Variables for the openMVG and openMVS binaries and the camera sensor database directory
OPENMVG_BIN = "C:/Users/Braden/Desktop/ECEN 404/OpenMVG/build"
OPENMVS_BIN = "C:/Users/Braden/Desktop/ECEN 404/OpenMVS/build"
CAMERA_SENSOR_DB_FILE = "sensor_width_camera_database.txt"
CAMERA_SENSOR_DB_DIRECTORY = "C:/Users/Braden/Desktop/ECEN 404/OpenMVG/sensor_width_database"

PRESET = {'SEQUENTIAL': [0,1,2,3,4,5,6,7,8,9,10]}

PRESET_DEFAULT = 'SEQUENTIAL'

# OBJECTS to store config and data in
class ConfContainer:
    """
        Container for all the config variables
    """
    def __init__(self):
        pass


class AStep:
    """ Represents a process step to be run """
    def __init__(self, info, cmd, opt):
        self.info = info
        self.cmd = cmd
        self.opt = opt


class StepsStore:
    """ List of steps with facilities to configure them """
    def __init__(self):
        self.steps_data = [
            ["Intrinsics analysis",          # 0
             os.path.join(OPENMVG_BIN, "openMVG_main_SfMInit_ImageListing"),
             #["-i", "%input_dir%", "-o", "%matches_dir%", "-d", "%camera_file_params%", "-f", str(1.2*500)]],
             ["-i", "%input_dir%", "-o", "%matches_dir%", "-d", "%camera_file_params%", "-f", str(1.2*3904)]],
             #["-i", "%input_dir%", "-o", "%matches_dir%", "-d", "%camera_file_params%", "-f", str(1.2*4032)]],
             #["-i", "%input_dir%", "-o", "%matches_dir%", "-d", "%camera_file_params%"]],
            ["Compute features",             # 1
             os.path.join(OPENMVG_BIN, "openMVG_main_ComputeFeatures"),
             ["-i", "%matches_dir%/sfm_data.json", "-o", "%matches_dir%", "-m", "SIFT", "-p", "ULTRA"]],
            #  ["-i", "%matches_dir%/sfm_data.json", "-o", "%matches_dir%", "-m", "SIFT"]],
            ["Compute pairs",                # 2
             os.path.join(OPENMVG_BIN, "openMVG_main_PairGenerator"),
             ["-i", "%matches_dir%/sfm_data.json", "-o", "%matches_dir%/pairs.bin"]],
            ["Compute matches",              # 3
             os.path.join(OPENMVG_BIN, "openMVG_main_ComputeMatches"),
             ["-i", "%matches_dir%/sfm_data.json", "-p", "%matches_dir%/pairs.bin", "-o", "%matches_dir%/matches.putative.bin", "-n", "AUTO"]],
            ["Filter matches",               # 4
             os.path.join(OPENMVG_BIN, "openMVG_main_GeometricFilter"),
             ["-i", "%matches_dir%/sfm_data.json", "-m", "%matches_dir%/matches.putative.bin", "-o", "%matches_dir%/matches.f.bin"]],
            ["Incremental reconstruction",   # 5
             os.path.join(OPENMVG_BIN, "openMVG_main_SfM"),
             ["-i", "%matches_dir%/sfm_data.json", "-m", "%matches_dir%", "-o", "%reconstruction_dir%", "-s", "INCREMENTAL"]],
             #["-i", "%matches_dir%/sfm_data.json", "-m", "%matches_dir%", "-o", "%reconstruction_dir%", "-s", "INCREMENTAL", "-f", "ADJUST_FOCAL_LENGTH|ADJUST_DISTORTION"]],
            ["Export to openMVS",            # 6
             os.path.join(OPENMVG_BIN, "openMVG_main_openMVG2openMVS"),
             ["-i", "%reconstruction_dir%/sfm_data.bin", "-o", "%mvs_dir%/scene.mvs", "-d", "%mvs_dir%/images"]],
            ["Densify point cloud",          # 7
             os.path.join(OPENMVS_BIN, "DensifyPointCloud"),
             ["scene.mvs", "--dense-config-file", "Densify.ini", "--resolution-level", "1", "--number-views", "8", "-w", "%mvs_dir%"]],
            ["Reconstruct the mesh",         # 8
             os.path.join(OPENMVS_BIN, "ReconstructMesh"),
             #["scene_dense.mvs", "-w", "%mvs_dir%", "--image-points-file",  "imagePoints.ini"]],
             ["scene_dense.mvs", "-w", "%mvs_dir%"]],
            ["Refine the mesh",              # 9
             os.path.join(OPENMVS_BIN, "RefineMesh"),
             ["scene_dense_mesh.mvs", "--scales", "1", "--gradient-step", "25.05", "-w", "%mvs_dir%"]],
            ["Texture the mesh",             # 10
             os.path.join(OPENMVS_BIN, "TextureMesh"),
             ["scene_dense_mesh_refine.mvs", "--decimate", "0.5", "-w", "%mvs_dir%"]],
            ]

    def __getitem__(self, indice):
        return AStep(*self.steps_data[indice])

    def length(self):
        return len(self.steps_data)

    def apply_conf(self, conf):
        """ replace each %var% per conf.var value in steps data """
        for s in self.steps_data:
            o2 = []
            for o in s[2]:
                co = o.replace("%input_dir%", conf.input_dir)
                co = co.replace("%output_dir%", conf.output_dir)
                co = co.replace("%matches_dir%", conf.matches_dir)
                co = co.replace("%reconstruction_dir%", conf.reconstruction_dir)
                co = co.replace("%mvs_dir%", conf.mvs_dir)
                co = co.replace("%camera_file_params%", conf.camera_file_params)
                o2.append(co)
            s[2] = o2


CONF = ConfContainer()
STEPS = StepsStore()

# ARGS
PARSER = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description="Photogrammetry reconstruction with these steps: \r\n" +
    "\r\n".join(("\t%i. %s\t %s" % (t, STEPS[t].info, STEPS[t].cmd) for t in range(STEPS.length())))
    )
PARSER.add_argument('input_dir',
                    help="the directory wich contains the pictures set.")
PARSER.add_argument('output_dir',
                    help="the directory wich will contain the resulting files.")
PARSER.add_argument('--steps',
                    type=int,
                    nargs="+",
                    help="steps to process")
PARSER.add_argument('--preset',
                    help="steps list preset in \r\n" +
                    " \r\n".join([k + " = " + str(PRESET[k]) for k in PRESET]) +
                    " \r\ndefault : " + PRESET_DEFAULT)

GROUP = PARSER.add_argument_group('Passthrough', description="Option to be passed to command lines (remove - in front of option names)\r\ne.g. --1 p ULTRA to use the ULTRA preset in openMVG_main_ComputeFeatures")
for n in range(STEPS.length()):
    GROUP.add_argument('--'+str(n), nargs='+')

PARSER.parse_args(namespace=CONF)  # store args in the ConfContainer


# FOLDERS
def mkdir_ine(dirname):
    """Make the folder if it doesn't exist"""
    if not os.path.exists(dirname):
        os.mkdir(dirname)


# Absolute path for input and ouput dirs
CONF.input_dir = os.path.abspath(CONF.input_dir)
CONF.output_dir = os.path.abspath(CONF.output_dir)

if not os.path.exists(CONF.input_dir):
    sys.exit("%s: path not found" % CONF.input_dir)

CONF.reconstruction_dir = os.path.join(CONF.output_dir, "sfm")
CONF.matches_dir = os.path.join(CONF.reconstruction_dir, "matches")
CONF.mvs_dir = os.path.join(CONF.output_dir, "mvs")
CONF.camera_file_params = os.path.join(CAMERA_SENSOR_DB_DIRECTORY, CAMERA_SENSOR_DB_FILE)

mkdir_ine(CONF.output_dir)
mkdir_ine(CONF.reconstruction_dir)
mkdir_ine(CONF.matches_dir)
mkdir_ine(CONF.mvs_dir)

# Update directories in steps commandlines
STEPS.apply_conf(CONF)

# PRESET
if CONF.steps and CONF.preset:
    sys.exit("Steps and preset arguments can't be set together.")
elif CONF.preset:
    try:
        CONF.steps = PRESET[CONF.preset]
    except KeyError:
        sys.exit("Unkown preset %s, choose %s" % (CONF.preset, ' or '.join([s for s in PRESET])))
elif not CONF.steps:
    CONF.steps = PRESET[PRESET_DEFAULT]

# WALK
# print("# Using input dir:  %s" % CONF.input_dir)
# print("#      output dir:  %s" % CONF.output_dir)
# print("# Steps:  %s" % str(CONF.steps))

for cstep in CONF.steps:

    # Retrieve "passthrough" commandline options
    opt = getattr(CONF, str(cstep))
    if opt:
        # add - sign to short options and -- to long ones
        for o in range(0, len(opt), 2):
            if len(opt[o]) > 1:
                opt[o] = '-' + opt[o]
            opt[o] = '-' + opt[o]
    else:
        opt = []

    # Remove STEPS[cstep].opt options now defined in opt
    for anOpt in STEPS[cstep].opt:
        if anOpt in opt:
            idx = STEPS[cstep].opt.index(anOpt)
            if DEBUG:
                print('#\tRemove ' + str(anOpt) + ' from defaults options at id ' + str(idx))
            del STEPS[cstep].opt[idx:idx+2]

    # create a commandline for the current step
    cmdline = [STEPS[cstep].cmd] + STEPS[cstep].opt + opt
    print('Cmd: ' + ' '.join(cmdline))

    if not DEBUG:
        # Launch the current step
        try:
            pStep = subprocess.Popen(cmdline)
            pStep.wait()
            if pStep.returncode != 0:
                break
        except KeyboardInterrupt:
            sys.exit('\r\nProcess canceled by user, all files remains')
    else:
        print('\t'.join(cmdline))
