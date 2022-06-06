#include <iostream>
#include <string>		// C++ style - find, substr, replace, length, size, npos
#include <algorithm>	// swap

#define npos std::string::npos
#include "position.hpp"


// #define C_STYLE

#ifdef C_STYLE
#include <cstring>	// C-style - strstr

void find_str(char const* str, char const* substr) 
{
    char* pos = strstr(str, substr);
    if(pos) 
	{
        std::cout << "Found the string \"" << substr << "\" in \"" << str << "\" at position: " << pos - str << std::endl;
    } 
	else 
	{
        std::cout << "The string \"" << substr << "\" was not found in \"" << str << '\"'<< std::endl;
    }
}
#endif

// pos - position
void print(std::string::size_type pos, std::string const &s, std::string::size_type count = npos)
{
    if (pos == npos) 
		std::cout << "The string was not found\n";
	
	else 
		// std::cout << "found: " << s.substr(n, count) << '\n';
		std::cout << "Found the string \"" << s.substr(pos, count) << "\" in \"" << s << "\" at position: " << pos << std::endl;
}

void print_str(std::string const &str)
{
	if (!str.empty()) std::cout << '\"' << str << '\"' << std::endl;
	else std::cout << "String is empty" << std::endl;
}


std::string replace_with(std::string str, const std::string &word, const std::string &new_word)
{
	std::string result_str;
	std::string::size_type pos;	// position
	
	pos = str.find(word);
	if (pos != npos) 
		result_str = str.replace(pos, word.size(), new_word);
	
	return result_str;	// returns empty string if failed
}

// replace text start with pos_1 to pos_2 inclusive
std::string replace_from(std::string str, const std::string &new_word, 
std::string::size_type pos_1 = npos, 
std::string::size_type pos_2 = npos)
{
	std::string result_str;
	
	if (pos_1 != npos || pos_2 != npos)
	{
		if (pos_1 == npos) pos_1 = pos_2;
		else if (pos_2 == npos) pos_2 = pos_1;
		
		if (pos_1 > pos_2) std::swap(pos_1, pos_2);
		
		result_str = str.replace(pos_1, (pos_2 - pos_1 + 1), new_word);
	}
	
	// std::cout << "pos_1:\t" << pos_1 << std::endl;
	// std::cout << "pos_2:\t" << pos_2 << std::endl;
	
	// std::string::const_iterator ipos_1 = str.begin() + pos_1;
	// std::string::const_iterator ipos_2 = str.begin() + pos_2 + 1;
	// result_str = str.replace(ipos_1, ipos_2, new_word);
	
	return result_str;
}

// replace text between str_begin and str_end
std::string replace_from(std::string str, const std::string &new_word, std::string str_begin, std::string str_end)
{
	std::string::size_type pos_1 = str.find(str_begin);
	std::string::size_type pos_2 = str.find(str_end);
	
	if (pos_1 != npos && pos_2 != npos)
		if (pos_1 > pos_2) 
		{
			std::swap(pos_1, pos_2);
			str_begin.swap(str_end);
		}
	
	if (pos_1 != npos) pos_1 += str_begin.size();	// -1 +1
	if (pos_2 != npos) pos_2 -= 1;					// 0 - 1 = npos
			
	return replace_from(str, new_word, pos_1, pos_2);
}


// std::string erase_d(std::string str, const std::string &new_word, std::string str_begin, std::string str_end)
// {
	

// }


int main()
{
	// std::string::size_type pos;
	// std::string str("Some string 1 (Eng)");
	// std::string str_repl("_TEXT_");
	// std::string new_str;
	
	// std::cout << str << std::endl << std::endl;

	// new_str = replace_from(str, str_repl, "(Eng)", "Some ");
	// print_str(new_str);
	// new_str = replace_from(str, "", "(Eng)", "Some ");
	// print_str(new_str);
	// new_str = replace_from(str, "", "S", "1");
	// print_str(new_str);
	
	position pos(0, 10);
	std::cout << pos << std::endl;
	position pos1('s', 'n', "string");
	std::cout << pos1 << std::endl;
	position pos2(3, 't', "string");
	std::cout << pos2 << std::endl;
	position pos3('g', 2, "string");
	std::cout << pos3 << std::endl;
	
	position pos4('b', 4, "string");
	std::cout << pos4 << std::endl;
	position pos5(1, 'd', "string");
	std::cout << pos5 << std::endl;

	
#ifdef C_STYLE
	std::cout << std::endl;
	char* c_str = "one two three";
    // find_str(c_str, "two");
    // find_str(c_str, "");
    // find_str(c_str, "nine");
    // find_str(c_str, "n");
	c_str = "Some string 1 (Eng)";
	find_str(c_str, "Eng");
#endif

	return 0;
}