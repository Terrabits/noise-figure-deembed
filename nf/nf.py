import skrf as rf

math_expression = 'linMag({input_trace})^2 * ({nf_trace} - (1/linMag({input_trace})^2)) - ((1/linMag({output_trace})^2)-1)/linMag({gain_trace})^2 + 1'

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

def calculate_deembedded_nf(input_s21_lin_mag, output_s21_lin_mag, gain_lin_mag, f_meas_lin_mag):
    assert len(input_s21_lin_mag) == len(output_s21_lin_mag) == len(gain_lin_mag) == len(f_total_lin_mag)
    # Clean up the names a little to make the math
    # more legible
    Fin   = 1.0 / input_s21input_s21_lin_mag
    Gin    = input_s21_lin_mag
    Fout  = 1.0 / output_s21_lin_mag
    Fmeas = f_meas_lin_mag
    Gdut = gain_lin_mag
    corrected_nf = Gin * (Fmeas - Fin) - ((Fout - 1.0) / (Gdut)) + 1
    return corrected_nf
