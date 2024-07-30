import numpy as np
import warnings
import flowkit as fk

# Paths
data1_fcs_path = 'data/gate_ref/data1.fcs'
fcs_path = 'data/gate_ref/data1.fcs'
gml_path = 'data/gate_ref/gml/gml_all_gates.xml'
fcs_file_path = "data/test_comp_example.fcs"
comp_file_path = "data/comp_complete_example.csv"
fcs_2d_file_path = "data/test_data_2d_01.fcs"
fcs_index_sorted_path = "data/index_sorted/index_sorted_example.fcs"
sample_id_with_spill = '101_DEN084Y5_15_E01_008_clean.fcs'
csv_8c_comp_file_path = 'data/8_color_data_set/den_comp.csv'
csv_8c_comp_null_channel_file_path = 'data/8_color_data_set/den_comp_null_channel.csv'


fcs_file_paths = [
    "data/100715.fcs",
    "data/109567.fcs",
    "data/113548.fcs"
]

# Samples

data1_sample = fk.Sample(data1_fcs_path)
data1_sample_with_orig = fk.Sample(data1_fcs_path, cache_original_events=True)
test_sample = fk.Sample(fcs_path, subsample=2000)
test_samples_base_set = fk.load_samples(fcs_file_paths)
test_samples_8c_full_set = fk.load_samples("data/8_color_data_set/fcs_files")
test_samples_8c_full_set_dict = {s.id: s for s in test_samples_8c_full_set}
sample_with_spill = test_samples_8c_full_set_dict[sample_id_with_spill]

test_gating_strategy = fk.parse_gating_xml(gml_path)

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    test_comp_sample = fk.Sample(
        fcs_path_or_data=fcs_file_path,
        compensation=comp_file_path,
        ignore_offset_error=True  # sample has off by 1 data offset
    )

    warnings.simplefilter('ignore')
    test_comp_sample_uncomp = fk.Sample(
        fcs_path_or_data=fcs_file_path,
        ignore_offset_error=True  # sample has off by 1 data offset
    )



# Coordinates, Dimensions, Gates, and Quadrants

ell1_coords = [12.99701, 16.22941]
ell1_cov_mat = [[62.5, 37.5], [37.5, 62.5]]
ell1_dist_square = 1

poly1_vertices = [
    [5, 5],
    [500, 5],
    [500, 500]
]
poly1_dim1 = fk.Dimension('FL2-H', compensation_ref='FCS')
poly1_dim2 = fk.Dimension('FL3-H', compensation_ref='FCS')
poly1_dims1 = [poly1_dim1, poly1_dim2]


poly1_gate = fk.gates.PolygonGate('Polygon1', poly1_dims1, poly1_vertices)

quad1_div1 = fk.QuadrantDivider('FL2', 'FL2-H', 'FCS', [12.14748])
quad1_div2 = fk.QuadrantDivider('FL4', 'FL4-H', 'FCS', [14.22417])
quad1_divs = [quad1_div1, quad1_div2]

quad_1 = fk.gates.Quadrant(
    quadrant_id='FL2P-FL4P',
    divider_refs=['FL2', 'FL4'],
    divider_ranges=[(12.14748, None), (14.22417, None)]
)
quad_2 = fk.gates.Quadrant(
    quadrant_id='FL2N-FL4P',
    divider_refs=['FL2', 'FL4'],
    divider_ranges=[(None, 12.14748), (14.22417, None)]
)
quad_3 = fk.gates.Quadrant(
    quadrant_id='FL2N-FL4N',
    divider_refs=['FL2', 'FL4'],
    divider_ranges=[(None, 12.14748), (None, 14.22417)]
)
quad_4 = fk.gates.Quadrant(
    quadrant_id='FL2P-FL4N',
    divider_refs=['FL2', 'FL4'],
    divider_ranges=[(12.14748, None), (None, 14.22417)]
)
quadrants_q1 = [quad_1, quad_2, quad_3, quad_4]

quad1_gate = fk.gates.QuadrantGate('Quadrant1', quad1_divs, quadrants_q1)

range1_dim1 = fk.Dimension('FSC-H', compensation_ref='uncompensated', range_min=100)
range1_dims = [range1_dim1]
range1_gate = fk.gates.RectangleGate('Range1', range1_dims)

range2_dim1 = fk.Dimension('Time', compensation_ref='uncompensated', range_min=20, range_max=80)
range2_dims = [range2_dim1]
range2_gate = fk.gates.RectangleGate('Range2', range2_dims)

ell1_dim1 = fk.Dimension('FL3-H', compensation_ref='uncompensated')
ell1_dim2 = fk.Dimension('FL4-H', compensation_ref='uncompensated')
ellipse1_dims = [ell1_dim1, ell1_dim2]



ellipse1_gate = fk.gates.EllipsoidGate('Ellipse1', ellipse1_dims, ell1_coords, ell1_cov_mat, ell1_dist_square)



# Transforms

asinh_xform1 = fk.transforms.AsinhTransform(
    'AsinH_10000_4_1',
    param_t=10000,
    param_m=4,
    param_a=1
)

hyperlog_xform1 = fk.transforms.HyperlogTransform(
    'Hyperlog_10000_1_4.5_0',
    param_t=10000,
    param_w=1,
    param_m=4.5,
    param_a=0
)

linear_xform1 = fk.transforms.LinearTransform(
    'Linear_10000_500',
    param_t=10000,
    param_a=500
)

logicle_xform1 = fk.transforms.LogicleTransform(
    'Logicle_10000_0.5_4.5_0',
    param_t=10000,
    param_w=0.5,
    param_m=4.5,
    param_a=0
)
logicle_xform2 = fk.transforms.LogicleTransform(
    'Logicle_10000_0.5_4_0.5',
    param_t=10000,
    param_w=0.5,
    param_m=4,
    param_a=0.5
)
logicle_xform3 = fk.transforms.LogicleTransform(
    'Logicle_10000_1_4_0.5',
    param_t=10000,
    param_w=1,
    param_m=4,
    param_a=0.5
)

xform_logicle = fk.transforms.LogicleTransform('logicle', param_t=10000, param_w=0.5, param_m=4.5, param_a=0)
xform_biex1 = fk.transforms.WSPBiexTransform('neg0', width=-100.0, negative=0.0)
xform_biex2 = fk.transforms.WSPBiexTransform('neg1', width=-100.0, negative=1.0)

# Spillover and Matrix

fcs_spill = '13,B515-A,R780-A,R710-A,R660-A,V800-A,V655-A,V585-A,V450-A,G780-A,G710-A,G660-A,G610-A,G560-A,'\
    '1,0,0,0.00008841570561316703,0.0002494559842740046,0.0006451591561972469,0.007198401782797728,0,0,'\
    '0.00013132619816952714,0.0000665251222573374,0.0005815839652764308,0.0025201730479353047,0,1,'\
    '0.07118758880093266,0.14844804153215532,0.3389031912802132,0.00971660311243448,0,0,0.3013801753249257,'\
    '0.007477611134717788,0.0123543122066652,0,0,0,0.33140488468849205,1,0.0619647566095391,0.12097867005182314,'\
    '0.004052554840959644,0,0,0.1091165124197372,0.10031383324016652,0.005831773047424356,0,0,0,'\
    '0.08862108746390694,0.38942413967608824,1,0.029758767352535288,0.06555281586224636,0,0,0.03129393154653089,'\
    '0.039305936245674286,0.09137451237674046,0.00039591122341817164,0.000056659766405160846,0,'\
    '0.13661791418865094,0.010757316236957385,0,1,0.00015647113960278087,0,0,0.48323487842103036,'\
    '0.01485813345103798,0,0,0,0,0.00012365104122837034,0.019462610460087203,0.2182062762553545,'\
    '0.004953221988365214,1,0.003582785726251024,0,0.0013106968243292993,0.029645575685206288,0.4089015923558522,'\
    '0.006505826616588717,0.00011917703878954761,0,0,0,0,0.001055595075733903,0.002287122431059274,1,0,'\
    '0.0003885172922042414,0.0001942589956485108,0,0.06255131165904257,0.13248446095817049,0,0,0,0,0,'\
    '0.008117870042687002,0.17006643956891296,1,0,0,0,0,0,0.003122390646560834,0.008525685683831916,'\
    '0.001024237027323255,0.0011626412849951272,0.12540105131097395,0.018142202256893485,0.19364562239714117,'\
    '0,1,0.06689784643460173,0.16145640353506588,0.2868231743828476,1.2380368696528024,0.002015498041918758,'\
    '0.06964529385206036,0.19471548842271394,0.0010077719457714136,0.15161117217667686,0.0012703511702660231,'\
    '0.007133491446011225,0,1.1500323358669722,1,0.016076827046672983,0.014674146885307975,0.055351746085494,'\
    '0.001685226072130514,0.05433993817875603,0.27785224557295884,0.34300826602551504,0.06175281041168121,'\
    '0.07752283973796613,0.0042628794531131406,0,0.49748791920091034,0.7439226300384197,1,0.010329232815907474,'\
    '0.03763461149817695,0,0.008713148000954844,0.04821275078920058,0.07319044343609345,0.1505631929508567,'\
    '0.3862934410767249,0.10189631814602482,0,0.3702770755789083,0.6134900271606913,1.2180240147472128,1,'\
    '0.06521131251063482,0.0016842378874079343,0,0,0.00009533732312150527,0.0034630076700367675,'\
    '0.01571183587491517,0.17412189188164517,0,0.023802192010810994,0.049474451704249904,0.13251071256825273,'\
    '0.23921555785727822,1'

fcs_spill_header = [
    'B515-A', 'R780-A', 'R710-A', 'R660-A',
    'V800-A', 'V655-A', 'V585-A', 'V450-A',
    'G780-A', 'G710-A', 'G660-A', 'G610-A',
    'G560-A'
]

spill01_fluoros = ['FITC', 'PE', 'PerCP']
spill01_detectors = ['FL1-H', 'FL2-H', 'FL3-H']
spill01_data = np.array(
    [
        [1, 0.02, 0.06],
        [0.11, 1, 0.07],
        [0.09, 0.01, 1]
    ]
)
comp_matrix_01 = fk.Matrix('MySpill', spill01_data, spill01_detectors, spill01_fluoros)

# pnn, pns lists

detectors_8c = [
    'TNFa FITC FLR-A',
    'CD8 PerCP-Cy55 FLR-A',
    'IL2 BV421 FLR-A',
    'Aqua Amine FLR-A',
    'IFNg APC FLR-A',
    'CD3 APC-H7 FLR-A',
    'CD107a PE FLR-A',
    'CD4 PE-Cy7 FLR-A'
]
fluorochromes_8c = [
    'TNFa',
    'CD8',
    'IL2',
    'Aqua Amine',
    'IFNg',
    'CD3',
    'CD107a',
    'CD4'
]
