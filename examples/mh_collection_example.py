
def wideMH():
    fields = []
    fields = fields + range(650, 500,-50)
    fields = fields + range(500,20,-10)
    fields = fields + dnp.arange(20,-20,-0.2).tolist()
    fields = fields + dnp.arange(-20,-500.1,-10).tolist()
    fields = fields + range(-500, -650,-50)

    pos pol pc
    scan vmag tuple(fields) refl 0.1
    scan vmag tuple(fields[::-1]) refl 0.1
    pos vmag 0
    pos pol nc
    scan vmag tuple(fields) refl 0.1
    scan vmag tuple(fields[::-1]) refl 0.1
    pos vmag 0
