from model.loss import torqueError
from model.model import AmbidexWristModel
from utils.Dynamics import *
from utils.LieGroup import *

eps = 1e-5


def test_dynamics():
    # fixture
    nJoint = 4
    nBatch = 2
    numel = nJoint * nBatch
    jointPos = torch.tensor([[0.100000000000, 0.200000000000, 0.300000000000, 0.400000000000],
                             [0.500000000000, 0.600000000000, 0.700000000000, 0.800000000000]])
    jointVel = torch.tensor([[1.300000000000, 1.400000000000, 1.500000000000, 1.600000000000],
                             [1.700000000000, 1.800000000000, 1.900000000000, 2.000000000000]])
    jointAcc = torch.tensor([[2.500000000000, 2.600000000000, 2.700000000000, 2.800000000000],
                             [2.900000000000, 3.000000000000, 3.100000000000, 3.200000000000]])
    A_screw = torch.tensor([[0.224441826344, 0.601482331753, 0.766710400581, 0.490734994411, -0.006495118141, -0.138559103012],
                            [0.610244035721, 0.603073656559, 0.513716280460, -0.012164890766, -0.367777347565, 0.446200340986],
                            [0.627912163734, 0.769596278667, 0.115965135396, 0.087397724390, -0.207147270441, 0.901492238045],
                            [0.135463878512, 0.220492705703, 0.965936064720, 0.164909064770, 0.573540449142, -0.154048174620]])
    initialLinkFrames = torch.eye(4).repeat(nJoint, 1, 1)
    Vdot0 = torch.tensor([0.0, 0.0, 0.0, 0.0, 9.81, 0.0])
    Phi = torch.tensor([9.049999713898e-01, 1.799999969080e-03, 1.327999979258e-01,
                        -3.999999898952e-04, 2.360000088811e-02, 4.100000020117e-03,
                        1.989999972284e-02, -3.000000142492e-04, 9.999999747379e-05,
                        -1.999999949476e-04, 5.608999729156e-01, 6.999999750406e-04,
                        1.955000013113e-01, 4.780000075698e-02, 7.680000364780e-02,
                        5.100000184029e-03, 7.190000265837e-02, -3.000000142492e-04,
                        -9.999999747379e-05, -1.669999957085e-02, 3.019999861717e-01,
                        -9.999999747379e-05, 1.632999926805e-01, -9.100000374019e-03,
                        9.019999951124e-02, 5.000000237487e-04, 8.969999849796e-02,
                        0.000000000000e+00, 0.000000000000e+00, 5.400000140071e-03,
                        2.433000057936e-01, 9.999999747379e-05, 1.451999992132e-01,
                        2.040000073612e-02, 8.919999748468e-02, 2.300000051036e-03,
                        8.690000325441e-02, 0.000000000000e+00, 0.000000000000e+00,
                        -1.190000027418e-02])
    F_ext = torch.zeros(6)
    # test function
    V, Vdot, linkFrames, jointTorque, F, W, Y = solveRecursiveDynamics(jointPos, jointVel, jointAcc, Phi, A_screw, initialLinkFrames, Vdot0, F_ext)

    # ground-truth
    V_matlab = torch.tensor([
        0.291774374247200, 0.781927031278900, 0.996723520755300, 0.637955492734300, - 0.008443653583300, - 0.180126833915600,
        1.114814057227452, 1.715669340014211, 1.648113433561892, 0.776204298597231, - 0.641547800476420, 0.521065608448550,
        1.752875388958052, 3.137072017794825, 1.695087573402299, 1.334684242774902, - 1.084354532305580, 2.128736757511019,
        2.893164824597505, 2.716963877596676, 3.287493913702312, 0.410045025245947, - 0.074057246335432, 2.336518968893387,
        0.381551104784800, 1.022519963980100, 1.303407680987700, 0.834249490498700, - 0.011041700839700, - 0.235550475120400,
        1.428022704743724, 2.427907101008026, 1.914338389675551, 1.330772222849376, - 1.135589416325381, 0.995065252195211,
        1.958603168336062, 4.527497957975128, 1.491839163861656, 2.542958879073361, - 1.568256554824447, 3.937889547865475,
        4.647847454511535, 2.564007568472893, 3.633429975551945, - 0.320125777258438, - 0.027372564807155, 5.035953429445052,
    ]).reshape(2, 4, 6)
    Vdot_matlab = torch.tensor([
        0.561104565860000, 1.503705829382500, 1.916776001452500, 1.984343569723769, 9.762483642587533, - 0.543607220627400,
        1.929949836162789, 3.849970344878574, 2.597502157353260, 4.352997071396117, 7.520461858731488, 0.395553479515355,
        1.794714489559869, 7.617274892552633, 1.611106033611643, 8.175501308802701, 6.039097045869843, 4.028459853519054,
        7.835740149741105, 3.344966955460686, 4.637881834087472, 4.635786811831605, 6.314463400282887, 6.450129552421065,
        0.650881296397600, 1.744298762083700, 2.223460161684900, 5.191217536358889, 9.024717377073038, - 0.903590930721940,
        2.559945716864191, 4.881461103265465, 2.112630434569490, 10.061014245558354, 3.750029511741489, 1.891169540717908,
        2.866129803721042, 9.146030043946430, - 1.114658566242805, 14.335364822229712, 3.536562443407326, 12.639026779443039,
        12.349726745874140, - 2.922467540512979, 3.623057474156147, 4.104947194016956, 2.015634934439369, 20.723291165389497
    ]).reshape(2, 4, 6)
    jointTorque_matlab = torch.tensor([
        7.541284654315438, -0.881243006890850, 5.794171320529918, -3.031369159197333,
        41.108143592680449, 5.402394957448899, 12.993583537240578, -8.751278068773706
    ]).reshape(2, 4)
    Y_matlab = torch.tensor([
        0.985700074870690, 0, 0, 0,
        8.007870327228371, 0, 0, 0,
        - 2.661800256346072, 0, 0, 0,
        - 0.255996548856723, 0, 0, 0,
        0.125935333531576, 0, 0, 0,
        0.904452488527565, 0, 0, 0,
        1.469612095897694, 0, 0, 0,
        0.674988965261455, 0, 0, 0,
        0.860409412916697, 0, 0, 0,
        2.305813797603683, 0, 0, 0,
        3.177628304360068, - 3.836234433305467, 0, 0,
        3.247112109279617, 2.730128971939640, 0, 0,
        - 5.246943890987688, - 0.659142261777435, 0, 0,
        6.295407227433706, - 3.480802697477088, 0, 0,
        0.251547415856237, 1.303231118917849, 0, 0,
        3.380692919965072, 1.578839489083939, 0, 0,
        1.191052112746883, 1.951864609049254, 0, 0,
        2.376930648778361, 3.223676413312525, 0, 0,
        1.249882602358126, 3.179757704793536, 0, 0,
        4.568422144178418, 3.473352763406504, 0, 0,
        13.295598598534312, - 1.663647270708724, - 1.344300607891049, 0,
        - 7.753358096239619, - 2.355149900264927, - 4.657585416127864, 0,
        - 5.554691066720239, - 3.598047214507359, 4.754479207641815, 0,
        20.236721502724087, 2.193700111237115, - 1.469868494862834, 0,
        - 0.861227957015912, 0.072583632000630, 2.775926745517141, 0,
        8.982163247048726, 5.341255274609509, 3.160913541107529, 0,
        - 0.987434432097455, 1.539941864792902, 1.239141312016794, 0,
        1.848606806011751, 3.692954980079083, 7.605970983524533, 0,
        - 1.784731645765323, 1.666103783129591, 3.902581458327432, 0,
        3.861249133036778, 6.449875795342670, 2.611102455247492, 0,
        6.657702021618492, - 0.279941475418610, 3.808499060381478, 1.580160279214328,
        - 16.829470744049257, 3.107425564361327, 5.243117445758147, 2.961364691426879,
        6.316190037727263, 11.775944764298313, 21.502586628177131, - 23.202167208651044,
        12.348811841093392, - 8.331135389319423, -13.438376037142843, 7.528787826004574,
        5.029890610460457, 5.658073527651606, 10.203137423382319, - 4.434236932166860,
        4.220881686624299, - 0.304107565885430, - 4.910627659700651, 7.120437674325124,
        - 1.541036353688352, 4.176487676234106, 3.769971581811490, 3.592697151489348,
        11.125362957063356, 4.247427309284956, 2.967257468790462, 3.816692122308392,
        5.181998448486752, 9.200099336888609, 11.791242532483800, 1.171564863278642,
        3.990180126648976, 3.098763272589129, - 2.611875974873420, 11.243641959644698,
        2.614096251988750, 0, 0, 0,
        7.690085490694787, 0, 0, 0,
        - 5.364279314177603, 0, 0, 0,
        1.957117572235631, 0, 0, 0,
        0.146084986896628, 0, 0, 0,
        1.049164886691975, 0, 0, 0,
        1.704750031241325, 0, 0, 0,
        0.782987199703288, 0, 0, 0,
        0.998074918983369, 0, 0, 0,
        2.674744005220272, 0, 0, 0,
        9.964653212263416, - 3.293138276461103, 0, 0,
        - 4.225812921141296, 1.397039099810075, 0, 0,
        - 5.622676232043836, - 4.036177800732931, 0, 0,
        15.205362499539705, 1.458958055708052, 0, 0,
        0.636571342207618, 1.429716291578091, 0, 0,
        4.971834140110254, 1.888675576514035, 0, 0,
        - 0.027683426782532, 2.272972983124233, 0, 0,
        3.863427226906697, 3.676845214563721, 0, 0,
        1.149801862336062, 3.312679679225083, 0, 0,
        3.795956659896046, 4.456062499868170, 0, 0,
        39.566677451147925, 6.038055692829156, 1.340655558916885, 0,
        - 31.272143852982651, -10.182102665053304, - 7.749864074029642, 0,
        11.531773744537006, - 7.062241522463172, 5.577806365598131, 0,
        29.587590673693853, 14.293760109504742, 5.106181773998966, 0,
        0.775055905662129, - 0.801153019809195, 3.020048058137570, 0,
        10.779635587202113, 8.785501219593245, 3.825973502123785, 0,
        - 2.858112154474208, - 0.191153792826842, 1.863145361178722, 0,
        5.489630412904623, 2.075454681095442, 9.379815856578585, 0,
        - 2.226750013097854, - 0.088718612955399, 3.177789166332715, 0,
        - 6.069921374388787, 5.030081085264584, 5.190795691523967, 0,
        44.047536151441342, 11.126044217502344, 18.373030362253473, - 13.412096016232267,
        - 20.134038298913449, 3.168340404069223, 23.762020712493388, - 23.907877958248388,
        60.002794631825530, 24.448511291775887, 36.774615019802560, - 35.563849489503291,
        8.095579659575282, - 4.228701889938712, -14.308646911288470, 11.732979987531834,
        17.696628296090935, 9.593946637387388, 11.723966771542530, - 6.114631448429289,
        - 5.810099652075924, - 2.088052080619269, - 6.877443739424944, 9.604788683029753,
        - 4.807149421922418, 2.812722358575561, 7.472258892975142, 1.038043752462901,
        5.065252011117902, 0.530430564357541, -13.002196761204587, 16.610039968736135,
        5.255686290153508, 10.446228136225706, 14.530115924422526, 3.183094106135147,
        - 7.333207101508346, - 0.941087086882924, - 4.575973373230343, 10.762861929281158,
    ]).reshape(2, 40, 4)
    Y_matlab = Y_matlab.transpose(1, 2)

    assert torch.all((V - V_matlab).abs() < eps), f'Error in V. V = {V}'
    assert torch.all((Vdot - Vdot_matlab).abs() < eps), f'Error in Vdot. Vdot = {Vdot}'
    assert torch.all((jointTorque - jointTorque_matlab).abs() < eps), f'Error in jointTorque. jointTorque = {jointTorque}'
    assert torch.all((jointTorque - Y @ Phi).abs() < eps), f'Error in jointTorque. jointTorque = {jointTorque}'
    assert Y.shape == (nBatch, nJoint, 10 * nJoint), f'Y.shape = {Y.shape}'
    assert torch.all((Y - Y_matlab).abs() < eps), f'Error in Y. Y.shape = {Y.shape}'

    U, S, V = torch.svd(Y.reshape(nBatch * nJoint, 10 * nJoint))
    pinvY = V[:, S > eps] @ S[S > eps].pow(-1).diag() @ U[:, S > eps].t()
    Phi_est = pinvY @ jointTorque.reshape(nBatch * nJoint, )  # (10*nJoint, nDynBatch*nMotor) @ (nDynBatch*nMotor,)

    assert torch.all((Y @ Phi_est - Y @ Phi).abs() < eps)


def test_torqueError1():
    nJoint = 4
    model = AmbidexWristModel(4, True)
    jointPos = torch.tensor([[0.0665, 0.1224, 0.1224, 0.0665],
                             [-0.1763, 0.0979, 0.0979, -0.1763]])
    jointVel = torch.tensor([[-0.2325, -0.0234, -0.0234, -0.2325],
                             [-0.6229, -0.0621, -0.0621, -0.6229]])
    jointAcc = torch.tensor([[-0.7617, -0.0764, -0.0764, -0.7617],
                             [-0.2946, -0.0227, -0.0227, -0.2946]])
    twists = torch.tensor([
        [-0.1809, -0.9367, -0.2996, 1.4146, -0.0655, -0.6495],
        [0.8698, -0.2895, 0.3995, 0.3160, 0.9867, 0.0269],
        [0.8803, -0.2890, 0.3761, 0.3392, 1.1042, 0.0546],
        [-0.1746, -0.9390, -0.2963, 1.4989, -0.0847, -0.6148]
    ])
    jacobian_theta = torch.tensor([
        [[0.0228, 0.0002],
         [0, 0.0227],
         [0, 0.0227],
         [0.0228, 0.0002]],

        [[0.0230, -0.0004],
         [0, 0.0227],
         [0, 0.0227],
         [0.0230, -0.0004]]
    ])
    motorTorque = torch.tensor([
        [- 0.0471, - 0.0414],
        [- 0.0524, - 0.0426]
    ])
    Vdot0 = torch.tensor([0.0, 0.0, 0.0, 0.0, 9.81, 0.0])
    jointState = State(jointPos, jointVel, jointAcc)
    motorPos, motorVel, motorAcc = torch.rand(2,2), torch.rand(2,2), torch.rand(2,2)
    motorState = State(motorPos, motorVel, motorAcc, motorTorque)
    assert torqueError(jointState, motorState, Vdot0, twists, jacobian_theta).abs() < eps


def test_torqueError2():
    nBatch = 40
    nJoint = 4
    nMotor = 2
    model = AmbidexWristModel(nJoint, True)
    motorPos, motorVel, motorAcc = torch.rand(nBatch, nMotor), torch.rand(nBatch, nMotor), torch.rand(nBatch, nMotor)
    motorState = State(motorPos, motorVel, motorAcc)
    jointState = model.getJointStates(motorState)
    jointPos, jointVel, jointAcc = jointState.pos, jointState.vel, jointState.acc
    Phi = torch.tensor([9.049999713898e-01, 1.799999969080e-03, 1.327999979258e-01,
                        -3.999999898952e-04, 2.360000088811e-02, 4.100000020117e-03,
                        1.989999972284e-02, -3.000000142492e-04, 9.999999747379e-05,
                        -1.999999949476e-04, 5.608999729156e-01, 6.999999750406e-04,
                        1.955000013113e-01, 4.780000075698e-02, 7.680000364780e-02,
                        5.100000184029e-03, 7.190000265837e-02, -3.000000142492e-04,
                        -9.999999747379e-05, -1.669999957085e-02, 3.019999861717e-01,
                        -9.999999747379e-05, 1.632999926805e-01, -9.100000374019e-03,
                        9.019999951124e-02, 5.000000237487e-04, 8.969999849796e-02,
                        0.000000000000e+00, 0.000000000000e+00, 5.400000140071e-03,
                        2.433000057936e-01, 9.999999747379e-05, 1.451999992132e-01,
                        2.040000073612e-02, 8.919999748468e-02, 2.300000051036e-03,
                        8.690000325441e-02, 0.000000000000e+00, 0.000000000000e+00,
                        -1.190000027418e-02])
    initialLinkFrames = torch.eye(4).repeat(nJoint, 1, 1)
    Vdot0 = torch.tensor([0.0, 0.0, 0.0, 0.0, 9.81, 0.0])
    F_ext = torch.zeros(6)
    twists = model.poe.getJointTwist()
    _, _, _, jointTorque, F, W, Y = solveRecursiveDynamics(jointPos, jointVel, jointAcc, Phi, twists, initialLinkFrames, Vdot0, F_ext)
    jacobian_theta = model.getJacobian(motorPos)

    motorTorque = (jacobian_theta.transpose(1, 2) @ jointTorque.view(nBatch, nJoint, 1)).squeeze()
    jointState = State(jointPos, jointVel, jointAcc)
    motorState = State(motorPos, motorVel, motorAcc, motorTorque)
    assert torqueError(jointState, motorState, Vdot0, twists, jacobian_theta).abs() < eps
