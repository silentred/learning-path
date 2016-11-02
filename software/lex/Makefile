lex:
	flex -l test.l
yacc:
	yacc -vd test.y 
cc:
	cc lex.yy.c y.tab.c -o exam -lm -ll

all: lex yacc cc

