OBJECTS= constructs.o mtrand.o
#WXFLAGS=`wx-config --cppflags --libs std,gl`
CPPFLAGS=-g3   -pthread -Wall $(WXFLAGS)


all: lamodel

run:
	make && ./lamodel && python vis.py

constructs.o: constructs.h

wxglmodel.o: constructs.h

wxglmodel: $(OBJECTS) wxglmodel.o  constructs.o
	g++   wxglmodel.o -o wxglmodel $(OBJECTS) -lm  -L/usr/local/lib/ $(WXFLAGS) -lGLU -lglut -lpthread -lGL

lamodel: $(OBJECTS) lamodel.o 
	g++  $(OBJECTS) lamodel.o -o lamodel -lm    -L/usr/local/lib/ # -lGLU -lglut 


tests: $(OBJECTS) tests.o 
	g++  $(OBJECTS) tests.o -o tests -lm    -L/usr/local/lib/ # -lGLU -lglut 


remake: clean all

cleanup:
	rm -f submit_lamodel.sh.e*
	rm -f submit_lamodel.sh.o*

clean: cleanup
	rm -f *.o lamodel.o* 

cdata:
	sh run_cluster.sh

data:
	sh run_serial.sh

figs:
	python an.py
	python two.py

