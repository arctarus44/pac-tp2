.PHONY: clean

coll_finder: lib/libcoll.a md5.o main.o
	g++ $^ -o $@

lib/libcoll.a:
	cd lib && $(MAKE)

clean:
	rm -f coll_finder
	rm -f *.o
	cd lib && $(MAKE) clean
