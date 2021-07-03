
def getInterpolator(start_x, end_x, power, y_lists):
	def function(t):
		return [polynomialSmoothing(start_x, end_x, pair[0], pair[1], t, power) for pair in y_lists]
	return function


def polynomialSmoothing(start_t, end_t, start_y, end_y, t, power):
	if t <= start_t:
		return start_y
	if t >= end_t:
		return end_y
	t_diff = end_t - start_t
	y_diff = end_y - start_y
	if t <= (start_t + end_t) / 2.0:
		scale = (2**(power - 1)) * y_diff / (t_diff**power)
		return (scale * ((t - start_t)**power)) + start_y
	else:
		scale = (2 ** (power - 1)) * y_diff * -1 / ((-1 * t_diff) ** power)
		return (scale * ((t - end_t) ** power)) + end_y
