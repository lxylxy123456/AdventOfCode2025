CXXFLAGS=-Wall -Werror -g -std=c++11 -pthread
LDFLAGS=-I include/

SOURCES := $(wildcard *.cpp)
TARGETS := $(patsubst %.cpp,%,$(SOURCES))

all: $(TARGETS)

$(TARGETS): %: %.cpp include/*.hpp

