.PHONY: clean

OBJ= block0.o block1stevens00.o block1stevens10.o block1wang.o md5.o block1.o block1stevens01.o block1stevens11.o main.o

coll_finder: lib/libcoll.a md5.o main.o
	g++ $OBJ -o $@ -L./lib

lib/libcoll.a:
	cd lib && $(MAKE)

clean:
	rm -f coll_finder
	rm -f *.o
	cd lib && $(MAKE) clean
