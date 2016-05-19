#!/usr/bin/env python
# coding=utf-8

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter as tefo	# allow to use new line within argparse strings

## parse script arguments
argparser = ArgumentParser(description='>> Conversion instrumental to standard photometry <<\n\n \
Requires Python 2 with:\n  * pylab\n  * scipy\n  * astropy\n  * argparse\n  * matplotlib\n\n', 
epilog='Authors: M.Kałuszyński & P.Bruś, ver. 2016-05-19', formatter_class=tefo)
argparser.add_argument('input_file', help='with the following structure:\n \
num_star ins_mag1 err_ins_mag1 std_mag1 err_std_mag1 ... ins_magN err_ins_magN \
std_magN err_std_magN\n\nnote:\n > mag1 ... magN should be sorted by growing \
wavelength\n > first line should be a comment preceded by # sign\n > the comment \
should contain the names of used passbands\n > pattern of a header for 3 \
passbands:\n   # no_star U_ins U_ierr U_std U_serr B_ins B_ierr B_std B_serr \
V_ins V_ierr V_std V_serr\n > the names in a header are used to assign the \
axes on charts\n > lack of the value in input_file should be signaled by 99.9999 \
(mags or errors)\n\n')
argparser.add_argument('output_file', help='will be produced having the following \
structure:\n num_star std(ins_mag1) err_ins_mag1 ... std(ins_magN) err_ins_magN\n\n\
note:\n > std(ins_mag) is an instrumental magnitude converted into a standard magnitude\n\
 > program makes output_file.log which contains parameters of conversions\n > program \
generates PNG figures illustrating each fitting')
argparser.add_argument('-s', help='float value of sigma for sigma clipping', dest='s', default=3)
argparser.add_argument('-i', help='number of iterations for sigma clipping.\nIf this option \
is turned on the program\ndoesn\'t display an interactive mode', dest='it', default=0)
args = argparser.parse_args()

from scipy import stats, odr
from pylab import *
from astropy.stats import sigma_clip
from matplotlib.cbook import Bunch
from matplotlib import pyplot as plt

######################################################################################################

# for sigma clipping
sigma = float(args.s)

# number of iterations
it = int(args.it)
if it < 0:
	it *= -1

# initial and final value of alpha for points
ini_alph = 0.6
fin_alph = 0.2

# initial and final label of the button
ini_buttstr = 'Finish?'
fin_buttstr = 'Done'

# none value in input_file should be marked by nocompl variable
nocompl = 99.9999

# to prevent setting err_mag = 0.0000 because of division by 1.0/err_mag^2 to compute weights
min_err_mag = 0.0001

######################################################################################################

# plots scatter chart on ax for color info Bunch c
def plot_color(b, ax, autoscale = True, state_scl = 0, legend = False):
	res = odr.ODR(odr.Data(b.icolor[b.ok], b.dmag[b.ok], 1.0/(b.err_icolor[b.ok] ** 2), 1.0/(b.err_dmag[b.ok] ** 2)), odr.Model(fun_odr), beta0=[b.a, b.b]).run()
	b.A = res.beta[0]
	b.B = res.beta[1]
	b.N = np.sum(b.ok)
	b.RMS = (res.res_var/b.N) ** 0.5
	ax.cla()
	ax.set_autoscale_on(autoscale)
	ax.autoscale(autoscale)
	fillcolor = ['b' if ok else 'r' for ok in b.ok]
	ax.scatter(b.icolor, b.dmag, c = fillcolor, alpha=b.alph, picker=5, label='stars')
	ax.plot(b.icolor, b.icolor * b.a + b.b, 'gray', alpha=0.2, label='initial regression')  # oryginal
	ax.plot(b.icolor, b.icolor * b.A + b.B, 'red', alpha=0.3, label='regression without rejected')  # actual
	ax.set_title(b.name + ' --- y = %.4fx + %.4f ------ RMS = %.4f --- N = %i' % (b.A, b.B, b.RMS, b.N), fontsize=20)
	ax.tick_params(axis='x', labelsize=13)
	ax.tick_params(axis='y', labelsize=13)
	ax.set_xlabel(b.xlab, fontsize=16)
	ax.set_ylabel(b.ylab, fontsize=16)
	if state_scl == 0:
		low = b.cur_low = b.ini_low
		upr = b.cur_upr = b.ini_upr
	elif state_scl == 1:
		low = b.dmag[b.ok].min()
		upr = b.dmag[b.ok].max()
		b.cur_low = low
		b.cur_upr = upr
	elif state_scl == 2:
		low = b.cur_low
		upr = b.cur_upr
	mrg = abs(upr - low) * 0.05 # 5% margin
	ax.set_ylim(low - mrg, upr + mrg)
	if legend:
		ax.legend()
	ax.figure.canvas.draw_idle()

# select new color to plot specified by button's ax (and plot)
def select_color(click_ax, plot_ax):
	plot_ax.col_data = click_ax.col_data
	donebutt.label.set_text(plot_ax.col_data.buttstr)
	plot_color(click_ax.col_data, plot_ax, state_scl=2)

# zoom in ignoring rejected points
def zoom_to_ok(plot_ax):
	plot_color(plot_ax.col_data, plot_ax, state_scl=1)

# reset zoom
def zoom_to_reset(plot_ax):
	plot_color(plot_ax.col_data, plot_ax)

# reject/unreject point manually on pick
def on_pick_point(event):
	ax = event.mouseevent.inaxes
	if ax.col_data.alph == ini_alph:
		ax.col_data.ok[event.ind] = not ax.col_data.ok[event.ind].any() ## if any point is ok change to rejected
		plot_color(ax.col_data, ax, autoscale=False, state_scl=2)

# freeze points and blocks operations on a chart
def frozen_plot(plot_ax):
	plot_ax.col_data.alph = fin_alph
	plot_ax.col_data.buttstr = fin_buttstr
	donebutt.label.set_text(plot_ax.col_data.buttstr)
	axbutts[plot_ax.col_data.idx].col_button.label.set_text('OK')
	plot_color(plot_ax.col_data, plot_ax, state_scl=2)

# model of function to ODR
def fun_odr(P,x):
	return P[0]*x + P[1]

# create a png image
def make_plot(b, output, fig, ax):
	ax.set_title(b.name + ' --- y = %.4fx + %.4f ------ RMS = %.4f --- N = %i' % (b.A, b.B, b.RMS, b.N), fontsize=20)
	xmin = b.icolor[b.ok].min()
	xmax = b.icolor[b.ok].max()
	xmrg = abs(xmin - xmax) * 0.05 # 5% margin
	ymin = b.dmag[b.ok].min()
	ymax = b.dmag[b.ok].max()
	ymrg = abs(ymin - ymax) * 0.4 # 30% margin
	ax.set_xlim(xmin - xmrg, xmax + xmrg)
	ax.set_ylim(ymin - ymrg, ymax + ymrg)
	ax.tick_params(axis='x', labelsize=13)
	ax.tick_params(axis='y', labelsize=13)
	ax.set_xlabel(b.xlab, fontsize=16)
	ax.set_ylabel(b.ylab, fontsize=16)
	ax.plot(b.icolor[b.ok], b.dmag[b.ok], 'bo', alpha = ini_alph)
	ax.plot(b.icolor[b.ok], b.icolor[b.ok] * b.A + b.B, 'red', alpha=0.5)
	fig.set_size_inches(16.0, 9.0, forward=True)
	fig.savefig(output.replace('.','_') + '-' + b.name.lower().replace('[','-').replace(']',''))

## load and extract data
# read header
out = args.output_file
fi = open(args.input_file, "r")
hr = fi.readline().replace('#','').replace('\r','').replace('\n','').split(' ')	# remove hashtags and whitespaces
fi.seek(0)	# set pointer at beginning of the input file
fi.close()	# obvious :)

# delete null strings
while hr.count(''):					# counter of null strings in the header list, each loop step decreases this value
	del hr[hr.index('')]			# method .index('') returns index of the first occurence of null string

# read data
D = np.loadtxt(args.input_file)		# "import numpy as np" during pylab import 
no = D[:,0]							# get the first column of D array, numbers indicating the stars
ismag = np.empty(len(no))
ismag.fill(nocompl)

# bunchlst - list of the Bunches, each Bunch represents 3 columns: instrumental mag, error of instr. mag and standard mag
Bunchlst = [Bunch(imag = D[:,i], err_imag = D[:,i+1], smag = D[:,i+2], err_smag = D[:,i+3]) for i in range(1, D.shape[1] - 1, 4)]

# search for incomplete pairs of mags, i.e. mags equal nocompl value
for b in Bunchlst:
	b.ismag = np.copy(ismag)
	b.compl = np.logical_not([1 if nocompl in [im,ie,sm,se] else 0 for im,ie,sm,se in zip(b.imag,b.err_imag,b.smag,b.err_smag)])
	for nr, i in enumerate(b.err_imag):
		if i < min_err_mag:
			b.err_imag[nr] = min_err_mag
	for nr, i in enumerate(b.err_smag):
		if i < min_err_mag:
			b.err_smag[nr] = min_err_mag

# only good points to calculate instrumental colors (needed because points come from two different Bunches)
for b1, b2 in zip(Bunchlst, Bunchlst[1:]):
	b1.filt = np.logical_and(b1.compl,b2.compl)
Bunchlst[-1].filt = Bunchlst[-2].filt

# calculate colors for each pair (by pairs iteration)
for b1, b2 in zip(Bunchlst, Bunchlst[1:]):
	b1.dmag = b1.smag[b1.filt] - b1.imag[b1.filt]
	b1.err_dmag = (b1.err_imag[b1.filt] ** 2 + b1.err_smag[b1.filt] ** 2) ** 0.5
	b1.icolor = b1.imag[b1.filt] - b2.imag[b1.filt]
	b1.err_icolor = (b1.err_imag[b1.filt] ** 2 + b2.err_imag[b1.filt] ** 2) ** 0.5
b_last = Bunchlst[-1]
b_last.dmag = b_last.smag[b_last.filt] - b_last.imag[b_last.filt]	# last
b_last.err_dmag = (b_last.err_imag[b_last.filt] ** 2 + b_last.err_smag[b_last.filt] ** 2) ** 0.5
Bunchlst[-1].icolor = Bunchlst[-2].icolor							# last
Bunchlst[-1].err_icolor = Bunchlst[-2].err_icolor					# last

# calculate initial model ax + b and reject status
for idx,b in enumerate(Bunchlst):
	res = odr.ODR(odr.Data(b.icolor, b.dmag, 1.0/(b.err_icolor**2), 1.0/(b.err_dmag**2)), odr.Model(fun_odr), beta0=[0.,0.]).run()
	ini_a = res.beta[0]
	ini_b = res.beta[1]
	res = odr.ODR(odr.Data(b.icolor, b.dmag, 1.0/(b.err_icolor**2), 1.0/(b.err_dmag**2)), odr.Model(fun_odr), beta0=[ini_a,ini_b]).run()
	b.a = b.A = res.beta[0]
	b.b = b.B = res.beta[1]
	b.ok = np.logical_not(sigma_clip((np.array(list(b.dmag))) - b.a * (np.array(list(b.icolor))) + b.b, sigma=sigma).mask)
	b.N = np.sum(b.ok)
	b.RMS = (res.res_var/b.N) ** 0.5
	# needed to mark frozen charts
	b.alph = ini_alph
	b.buttstr = ini_buttstr
	# needed to set proper scale
	b.ini_low = b.cur_low = b.dmag.min()
	b.ini_upr = b.cur_upr = b.dmag.max()
	# idx needed to mark switchers by 'OK' label
	b.idx = idx

# labels of axes and charts
for i, b in enumerate(Bunchlst[:-1]):
	j = 4 * i + 1
	b.name = 'Equation[' + str(i+1) + ']'
	b.xlab = hr[j] + ' - ' + hr[j+4]
	b.ylab = hr[j+2] + ' - ' + hr[j]
Bunchlst[-1].name = 'Equation[' + str(i+2) + ']'
Bunchlst[-1].xlab = Bunchlst[-2].xlab			# last
Bunchlst[-1].ylab = hr[-2] + ' - ' + hr[-4]		# last

if not it:
	fig, plotax = subplots()

	# switcher
	subplots_adjust(bottom=0.2)
	axbutts = [axes([0.1 + i*0.05, 0.05, 0.05, 0.075]) for i in range(len(Bunchlst))]
	for i, ax in enumerate(axbutts):
		ax.col_button = Button(ax, str(i + 1))
		ax.col_button.on_clicked(lambda event: select_color(event.inaxes, plotax))
		ax.col_data = Bunchlst[i]

	# zoom button - ignores rejected
	axzoom = axes([0.66, 0.05, 0.08, 0.075])
	zoombutt = Button(axzoom, "Zoom +")
	zoombutt.on_clicked(lambda event: zoom_to_ok(plotax))

	# zoom reset button
	axreset = axes([0.74, 0.05, 0.08, 0.075])
	resetbutt = Button(axreset, "Zoom -")
	resetbutt.on_clicked(lambda event: zoom_to_reset(plotax))

	# finish selection
	axdone = axes([0.82, 0.05, 0.08, 0.075])
	donebutt = Button(axdone, ini_buttstr)
	donebutt.on_clicked(lambda event: frozen_plot(plotax))

	# loop to calculate all values for each charts, initially -1 is assigned to RMS and N variables
	for i in axbutts[::-1]:
		select_color(i, plotax)
	fig.canvas.mpl_connect('pick_event', on_pick_point)
	show()

else:
	for b in Bunchlst:
		for i in range(it):
			b.ok = np.logical_not(sigma_clip((np.array(list(b.dmag))) - b.A * (np.array(list(b.icolor))) + b.B, sigma=sigma).mask)
			res = odr.ODR(odr.Data(b.icolor[b.ok], b.dmag[b.ok], 1.0/(b.err_icolor[b.ok] ** 2), 1.0/(b.err_dmag[b.ok] ** 2)), odr.Model(fun_odr), beta0=[b.a, b.b]).run()
			b.A = res.beta[0]
			b.B = res.beta[1]
			b.N = np.sum(b.ok)
			b.RMS = (res.res_var/b.N) ** 0.5

# make a name of a log file
log = out
while log.count('.'):
	log = log[:out.rfind('.')]
	if log[-1] != '.':
		break

if log+'.log' != out:
	log += '.log'
else:
	tmp = out
	out = log
	log = tmp

# save png images
for b in Bunchlst:
	fig, plotax = plt.subplots()
	make_plot(b, out, fig, plotax)

# create a log file
dl = open(log, "w")
dl.write("# Eq_num  A_coeff  B_coeff  N_stars  RMS/star\n")
for b in Bunchlst:
	dl.write("%2s %8.4f %8.4f %6d %7.4f\n" % (b.name.replace('Equation[','').replace(']',''), b.A, b.B, b.N, b.RMS))
dl.close()

# calculate standard magnitudes
for b1,b2 in zip(Bunchlst, Bunchlst[1:]):
	for idx,(i,j) in enumerate(zip(b1.imag,b2.imag)):
		if b1.imag[idx] != nocompl and b2.imag[idx] != nocompl:
			b1.ismag[idx] = b1.imag[idx] + b1.A * (b1.imag[idx] - b2.imag[idx]) + b1.B

# the last pair of passbands
for b1,b2 in zip(Bunchlst[-2:-1],Bunchlst[-1:]):
	for idx,(i,j) in enumerate(zip(b1.imag,b2.imag)):
		if b1.imag[idx] != nocompl and b2.imag[idx] != nocompl:
			b2.ismag[idx] = b2.imag[idx] + b2.A * (b1.imag[idx] - b2.imag[idx]) + b2.B

# save standard magnitudes into output file
FmtList = []
FmtList.append('%7d')
OutArr = []
OutArr.append(no)

for i in range(len(Bunchlst)):
	FmtList.append('%10.4f')
	FmtList.append('%7.4f')

for b in Bunchlst:
	OutArr.append(b.ismag)
	OutArr.append(b.err_imag)

np.savetxt(out, array(OutArr).T, fmt=FmtList)
