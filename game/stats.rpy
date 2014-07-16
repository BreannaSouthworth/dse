#init:
#    style stats_frame is frame:
    

init -100 python:

    __dse_stats = [ ]

    class __Stat(object):

        def __init__(self, name, var, default, max):
            self.name = name
            self.var = var
            self.default = default
            self.max = max

    def __init_stats():
        for s in __dse_stats:
            setattr(store, s.var, s.default)

    config.start_callbacks.append(__init_stats)
            
    def register_stat(name, var, default, max):
        __dse_stats.append(__Stat(name, var, default, max))

    def normalize_stats():
        for s in __dse_stats:

            v = getattr(store, s.var)

            if v > s.max:
                v = s.max
            if v < 0:
                v = 0

            setattr(store, s.var, v)

screen display_stats(name=True, bar=True, value=True, max=True):
    $ dse_stat_length = len(__dse_stats)
    window:
        yalign 0.0
        xalign 0.5

        vbox:
            yalign 0.0
            xalign 0.5
            label "Statistics"

            grid 3 dse_stat_length:
                xalign 0.5
                yalign 0.5
                spacing 5
                
                for s in __dse_stats:
                    $ v = getattr(store, s.var)

                    if name:
                        label s.name
                    
                    if bar:
                        bar value v range s.max xmaximum 150 xalign 0.0
                        
                    if value and max:
                        label ("%d/%d" % (v, s.max)) xalign 1.0
                    elif value:
                        label ("%d" % (v,)) xalign 1.0
                    elif max:
                        label ("%d" % (max,)) xalign 1.0
