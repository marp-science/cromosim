# Authors:
#     Sylvain Faure <sylvain.faure@universite-paris-saclay.fr>
#     Bertrand Maury <bertrand.maury@universite-paris-saclay.fr>
# License: GPL

import numpy as np
import numpy as sp        # import scipy as sp
import sys
import random
import matplotlib
import matplotlib.pyplot as plt

from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Arc, Polygon, Wedge
from matplotlib.collections import LineCollection, PatchCollection

def iteration(it,Nrooms,DoorRoomCapacity,NPir,NPrir,NPwir,Nior,List_iOr,T_iOr,Flux):
    """
        To run one iteration (which corresponds to 1 second) of the compartment \
        model. The compartments shall be identified to nodes of a network, those \
        nodes are connected by edges, which correspond to paths between nodesself.

    Parameters
    ----------
    it: integer
        iteration number
    Nrooms: int
        number of rooms
    DoorRoomCapacity: numpy array
        capacities of each door (number of persons per second)
    NPir: numpy array
        numbers of persons for each room
    NPrir: numpy array
        inlets for each room
    NPwir: numpy array
        numbers of persons who are waiting to leave each room
    Nior: numpy array
        numbers of inlets for each room
    List_iOr: numpy array
        room numbers associated to the inlets for each room
    T_iOr: numpy array
        travel times to cross each room
    Flux: numpy array
        numbers of persons upstream the exits

    Returns
    -------
    Flux: numpy array
        new numbers of persons upstream the exits
    NPir: numpy array
        new numbers of persons for each room
    NPwir: numpy array
        new numbers of persons who are waiting to leave each room
    NPrir: numpy array
        new inlets for each room
    """
    for ir in np.arange(Nrooms):
        Flux[it,ir]=min(DoorRoomCapacity[ir],NPwir[it-1,ir])

    for ir in np.arange(Nrooms):
        NPir[it,ir]  =  NPir[it-1,ir]-Flux[it,ir]
        NPwir[it,ir] =  NPwir[it-1,ir]-Flux[it,ir]
        for k in np.arange(Nior[ir]):
            NPir[it,ir] += Flux[it,int(List_iOr[ir,k])]
            timelag = int(T_iOr[ir,k])
            if timelag < it:
                NPwir[it,ir]+=Flux[it-timelag,int(List_iOr[ir,k])]
            NPrir[ir,k] = 0
            for i in np.arange(min(it,timelag)):
                NPrir[ir,k] += Flux[it-i,int(List_iOr[ir,k])]
    return Flux,NPir,NPwir,NPrir


def plot_compt(ifig, RoomNames, RoomCenters, DoorCenters, CircAngles, NPir,
               NPrir, NPwir, Nior,List_iOr, dom, area, savefig=False,
               filename='fig.png', title=''):
    """
    To draw

    Parameters
    ----------
    ifig: int
        figure number
    RoomNames: list
        number of rooms
    RoomCenters: numpy array
        coordinates of the room centers
    DoorCenters: numpy array
        coordinates of the door centers
    CircAngles: numpy array
        rotational angles of the half-disks localized at each door
    NPir: numpy array
        numbers of persons for each room
    NPrir: numpy array
        inlets for each room
    NPwir: numpy array
        numbers of persons who are waiting to leave each room
    Nior: numpy array
        numbers of inlets for each room
    List_iOr: numpy array
        room numbers associated to the inlets for each room
    dom: Domain
        contains everything for managing the domain
    area: float
        typical area size in m^2 of one individual
    savefig: boolean
        writes the figure as a png file if true
    filename: string
        png filename used to write the figure
    title: string
        title of the figure
    """
    Nr = DoorCenters.shape[0]
    plt.figure(ifig)
    plt.clf()
    ax0 = plt.subplot(111)
    cf0 = ax0.imshow(dom.image,interpolation='nearest',
               extent=[dom.xmin,dom.xmax,dom.ymin,dom.ymax], origin='lower')

    circles0 = [];
    colors0 = [];
    m2 = NPir*area ## surface demi-cercle = pi*R^2/2 = m2 => R = sqrt(2*m2/pi)
    R = np.sqrt(2*m2/np.pi)
    scale = 1
    for id,name in enumerate(RoomNames):
        wedge = Wedge((DoorCenters[id,0], DoorCenters[id,1]), R[id],
                0+CircAngles[id], 180+CircAngles[id], ec="none")
        circles0.append(wedge)
        ax0.text(RoomCenters[id,0], RoomCenters[id,1],
                 str(int(NPir[id])), fontsize=10)
        #arc = Arc((DoorCenters[id,0], DoorCenters[id,1]),  \
        #                             R[id],  R[id], theta1=0, theta2=180, \
        #                             angle=CircAngles[id], color='k')
        #circles0.append(arc)
        colors0.append(0.0)
    for ir in np.arange(Nr):
        for id in np.arange(Nior[ir]):
            jr = List_iOr[ir,id]
            xx0 = DoorCenters[ir,0]
            yy0 = DoorCenters[ir,1]
            xx1 = DoorCenters[jr,0]
            yy1 = DoorCenters[jr,1]
            ## line: [xx0, yy0, xx1, yy1]
            len = np.sqrt( (xx0-xx1)**2+(yy0-yy1)**2 )
            s = 0.5*NPrir[ir,id]*area/len
            circles0.append(Polygon( np.array([[xx0-s,yy0],[xx0+s,yy0], \
                                               [xx1+s,yy1],[xx1-s,yy1]]), \
                                     closed=True, fill=True))
            colors0.append(1.0)
    # for line in Lines:
    #     ##l: [xx0, yy0, xx1, yy1]
    #     s = l[]
    #     circles0.append(Polygon(np.array([[],[]]), True)

    patches0 = PatchCollection(circles0, cmap=matplotlib.cm.prism, alpha=0.6,
                               linewidth=0)
    patches0.set_array(np.array(colors0))
    ax0.add_collection(patches0)
    ax0.set_xticks([])
    ax0.set_yticks([])
    ax0.axis('off')
    ax0.set_title(title)
    plt.draw()
    if savefig:
        plt.savefig(filename, dpi=300)
    plt.pause(0.1)
