#include "Compare.h"

int cmp::ICompare::compare_and_out(const couple_t &file_1, const couple_t &file_2)
{
	int result = 0;
	
	if (file_1.second != file_2.second)
	{
		if (file_1.second > file_2.second)
		{
			diff = file_1.second - file_2.second)/1024;
			p_color1 = green;
			p_color2 = red;
			result = 1;
		}
		else
		{
			diff = file_2.second - file_1.second)/1024;
			p_color1 = red;
			p_color2 = green;
			result = 2;
		}
	}
	else
	{
		diff = 0;
		p_color1 = white;
		p_color2 = white;
		// result = 0;
	}
	
	std::cout 
	<< file_1.first.filename().string() 
	<< '\t' << p_color1 << file_1.first.parent_path().filename().string() << reset
	<< '\t' << p_color2 << file_2.first.parent_path().filename().string() << reset 
	<< '\t' << diff << " Kb" << std::endl;
	
	return result;
}

void compare(const couple_t &file_1, const couple_t &file_2) override
{
	compare_and_out(file_1, file_2);
}