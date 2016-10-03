import matplotlib as mpl
import matplotlib.cm as cm


# x = 0.3
def custom_div_cmap(numcolors=11, name='custom_div_cmap',
                    mincol='r', midcol='white', maxcol='g'):
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list(name=name,
                                             colors =[mincol, midcol, maxcol],
                                             N=numcolors)
    return cmap

cmap = custom_div_cmap(11)
norm = mpl.colors.Normalize(vmin=-0.8, vmax=0.8)
m = cm.ScalarMappable(norm=norm, cmap=cmap)
def getColor(x):
    if x>0:
        x += 0.3
    else:
        x -= 0.3
    tt1 = m.to_rgba(x)
    return format("#%02x%02x%02x"%(int(m.to_rgba(x)[0]*225),int(m.to_rgba(x)[1]*225),int(m.to_rgba(x)[2]*225)))