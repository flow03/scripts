#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <cstring>

int main()
{
	char* ostype = getenv("OSTYPE");
	
#ifdef OS
	if (ostype == NULL)
	{
		// не угадали. попробуем, а вдруг это виндовс!?
		ostype = getenv("windir");
		if (ostype != NULL)
		{ 
			//printf("windows catalog is found!!! yo!\n");
			std::cout << "windir\t" << ostype << std::endl;
		}
	}
#endif

	ostype = getenv("windir");
	std::cout << "windir\t" << ostype << std::endl;
	
	ostype = getenv("OS");
	std::cout << "OS\t" << ostype << std::endl;
	
	ostype = getenv("ComSpec");
	std::cout << "ComSpec\t" << ostype << std::endl;
	
	ostype = getenv("Path");
	std::cout << "Path\t" << ostype << std::endl;
	
}