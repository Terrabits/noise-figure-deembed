import numpy as np
import skrf  as rf

math_expression = 'linMag({input_trace})^2 * ({nf_trace} - (1/linMag({input_trace})^2)) - ((1/linMag({output_trace})^2)-1)/linMag({gain_trace})^2 + 1'

def f_to_db(mag):
    return 10.0 * np.log10(mag)

def read_s21_complex(filename, interpolated_freq_Hz=None):
    n = rf.Network(filename)
    if interpolated_freq_Hz:
        new_freq = n.Frequency()
        new_freq.f = interpolated_freq_Hz
        n = n.interpolate(new_freq)
    return n.s21.s.flatten()

def create_memory_trace(vna_obj, name, channel, s21_complex):
    data_name = '_{0}'.format(name)
    vna_obj.create_trace(data_name, channel, 's21')
    vna_obj.trace(data_name).to_memory(name)
    vna.trace(name).write_complex(s21_complex)

def apply_math(input_trace, output_trace, gain_trace, nf_trace):
    params = dict()
    params['input_trace' ] = input_trace
    params['output_trace'] = output_trace
    params[  'gain_trace'] =   gain_trace
    params[    'nf_trace'] =     nf_trace
    vna.trace(nf_trace).set_math(math_expression.format_map(params))

def calculate_deembedded_nf(Gin, Gout, Gdut, Fmeas):
    assert len(Gin) == len(Gout) == len(Gdut) == len(Fmeas)
    Fin   = 1.0 / Gin
    Fout  = 1.0 / Gout
    return Gin * (Fmeas - Fin) - ((Fout - 1.0) / (Gdut)) + 1
