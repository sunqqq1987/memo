# ARM 伪指令 #

	参考 
	http://xp9802.iteye.com/blog/2012231

	
- .section

	格式

		.section section_name[,"flags"[,%type[,flag_specific_arguments]]] 
	
	作用

		定义一个段，每一个段以段名为开始，以下一个段名或者文件结尾为结束。

		ELF格式允许的段标志： a：可分配的段, w：可写段, x：执行段
	
	举例

		.section .mysection 　　@自定义数据段，段名为“.mysection”

	Assembler.h (\kernel\arch\arm64\include\asm):

		#define USER(l, x...)				\
		9999:	x;					\
		.section __ex_table,"a";		\  //可以分配的__ex_table section
		.align	3;				\
		.quad	9999b,l;			\
		.previous


- .align

		.align  //指令就对齐
	
- adr 和 ldr

		https://blog.csdn.net/linweig/article/details/5411655
		https://blog.csdn.net/zhou1232006/article/details/6145039