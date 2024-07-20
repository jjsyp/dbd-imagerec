from screen.tracking import track_loop
import cProfile

pr = cProfile.Profile()
pr.enable()



track_loop()

pr.disable()
pr.print_stats(sort='cumtime')

#cProfile.run("track_loop()", filename="my_program.prof") 
                       