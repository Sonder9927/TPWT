# author: sonder
# created: 11 June 2022
# version: 1.0.1
import pygmt
from icecream import ic
import os
import pandas as pd

def make_cpt(VEL_CPT):
    pygmt.makecpt(cmap="dp/gridvel_6_v3.cpt", series=[-5, 5, 0.05], background="", continuous="", output=VEL_CPT)
    pygmt.makecpt(cmap="seis", series=[3.3, 3.9, 0.1], background="", continuous="", output="dp/test2.cpt")
    pygmt.makecpt(cmap="hot", series=[0, 80, 2.5], background="", continuous="", output="dp/std.cpt")

def make_gra(region, TOPO_GRA):
    TOPO_GRD = 'dp/topo.grd'
    TOPO_GRD2 = 'dp/topo.grd2'

    pygmt.grdcut(grid="dp/ETOPO1.grd", region=region, outgrid=TOPO_GRD)
    pygmt.grdsample(grid=TOPO_GRD, outgrid=TOPO_GRD2, spacing="0.01", region=region)
    pygmt.grdgradient(grid=TOPO_GRD2, azimuth=45, outgrid=TOPO_GRA, normalize="t", verbose="")

def average(file):
    '''
    read the velocity and calculate the average value
    return avevel and title
    '''
    df = pd.read_csv(file, sep="\s+", header=None, names=["la", "lo", "vel"], engine="python")
    avevel = df["vel"].sum() / len(df)
    # format title. The process needs to be improved with regularization in the future
    title = "%s vel=%5.4f" % (os.path.basename(file), avevel)
    return avevel, title

def dp_title_and_tmpgrd(per, region):
    # get TOMO_VEL file and format title
    files = os.listdir('dp/{}/new_2d'.format(per))
    for f in files:
        if "grid." in f and not f.endswith(".ave"):
            TOMO_VEL = "dp/{}/new_2d/{}".format(per, f)
            _, title = average(TOMO_VEL)

    # grid from TOMO_VEL will used in grdimage
    pygmt.blockmean(
        data = TOMO_VEL + ".ave",
        region = region,
        spacing = "0.25/0.25",
        outfile = "dp/ttmp"
    )

    pygmt.surface(
        data = "dp/ttmp",
        outgrid = "dp/tmp.grd",
        region = region,
        spacing = "0.5",
    )

    pygmt.grdsample(
        grid = "dp/tmp.grd",
        spacing = "0.01",
        outgrid = "dp/tmp2.grd",
    )
    return title

def dp_grid(per, region, projection, VEL_CPT, TOPO_GRA):
    # get title and create tmp2.grd
    title = dp_title_and_tmpgrd(per, region)

    # Initial the intance
    fig = pygmt.Figure()

    # Define figure configuration
    pygmt.config(
        MAP_FRAME_TYPE = "plain",
        MAP_TITLE_OFFSET = "0.25p",
        MAP_DEGREE_SYMBOL = "none",
    )

    # plot
    fig.coast(
        region = region,
        projection = projection,
        frame = [f'WSne+t"{title}"', "xa2f2", "ya2f2"],
        area_thresh = 10000,
        land = "white",
        shorelines = "",
        resolution = "l",
    )

    # grdimage
    fig.grdimage(
        grid = "dp/tmp2.grd",
        cmap = VEL_CPT,
        shading = TOPO_GRA,
    )

    # plot china textonics
    fig.plot(data="dp/China_tectonic.dat", pen="thick,black,-")
    # plot weihe
    fig.plot(data="dp/weihe1.txt", pen="thick,black,-")
    fig.plot(data="dp/weihe2.txt", pen="thick,black,-")

    # plot station
    df_station = pd.read_csv("dp/station.lst", sep="\s+", header=None, names=["la", "lo"], index_col=0, engine="python")
    fig.plot(
        data = df_station,
        pen = "black",
        style = "t0.1c",
        color = "blue",
    )

    # plot colorbar
    fig.colorbar(
        cmap = VEL_CPT,
        position = "jMR+v+w6c/0.2c+o-1c/0c+m",
        frame = "xa2f2"
    )

    return fig

# preparing
def dp_std():
    ic()

def dp_plot(per, region):
    # setting
    TOPO_GRA = 'dp/topo.gradient'
    VEL_CPT = 'dp/test.cpt'

    # grdgradient to get TOPO_GRA
    make_gra(region, TOPO_GRA)
    # makecpt to get VEL_CPT
    make_cpt(VEL_CPT)

    projection = "m{}/{}/0.7i".format(region[0], region[2])

    # create an instance of the Figure class and plot grid
    fig = dp_grid(per, region, projection, VEL_CPT, TOPO_GRA)

    # move
    #fig.shift_origin(yshift = "-12c")

    # plot std
    #fig = dp_std(fig, per, region, projection, VEL_CPT)
    dp_std()

    # save figure
    fig.savefig(f"grid{per}.pdf")

def shanghai():
    region = [118, 123, 29, 32]

    # period figure
    per = [20, 25, 30]
    for i in per:
        dp_plot(i, region)

if __name__ == "__main__":
    shanghai()
