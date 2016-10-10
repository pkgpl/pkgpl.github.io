from gpl.psplot import plot

vel="marm16km.drt"
opt="n1=188 d1=0.016 d2=0.016 d1num=1 d2num=2"

plot.velocity("vel.png",vel,opt+"lbeg=1.5 lend=5.5 lfnum=1.5")
plot.velocity_color("vel_color.png",vel,opt)
plot.velocity_color("density_color.png",vel,opt,unit="g/cc")
plot.gradient("grad.png",vel,opt)
plot.gradient_color("grad_color.png",vel,opt)
plot.migration("mig.png",vel,opt)
plot.contour("contour.png",vel,opt)

seismo="marm3000.su"
opt2="f2=0 d2=0.025 d1s=0.5 d2s=0.5"
plot.seismogram("seismo.png",seismo,opt2)

spec="marm3000fx.su"
plot.spectrum("spec.png",spec,opt2)
