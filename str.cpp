#include <iostream>
#include <string>		// C++ style - find, substr, replace, length, size, npos
#include <algorithm>	// swap

#define npos std::string::npos
#include "position.hpp"


// #define C_STYLE
typedef std::string::size_type st;

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
void print(st pos, std::string const &s, st count = npos)
{
    if (pos == npos) 
		std::cout << "The string was not found\n";
	
	else 
		std::cout << "Found the string \"" << s.substr(pos, count) << "\" in \"" << s 
		<< "\" at position: " << pos << std::endl;
}

void print_str(std::string const &str)
{
	if (!str.empty()) std::cout << '\"' << str << '\"' << std::endl;
	else std::cout << "String is empty" << std::endl;
}


std::string replace_with(std::string str, const std::string &word, const std::string &new_word)
{
	std::string result_str;
	st pos;	// position
	
	pos = str.find(word);
	if (pos != npos) 
		result_str = str.replace(pos, word.size(), new_word);
	
	return result_str;	// return empty string if failed
}

// replace text start with pos_1 to pos_2 inclusive
std::string replace_from(std::string str, const std::string &new_word, position pos)
{
	// std::string result_str;
	
	// result_str = str.replace(pos.get_pos1(), (pos.get_pos2() - pos.get_pos1() + 1), new_word);
	
	
	std::cout << pos << std::endl;
	
	// std::string::const_iterator ipos_1 = str.begin() + pos_1;
	// std::string::const_iterator ipos_2 = str.begin() + pos_2 + 1;
	// result_str = str.replace(ipos_1, ipos_2, new_word);
	
	return str.replace(pos.get_pos1(), (pos.get_pos2() - pos.get_pos1() + 1), new_word);
}

// replace text between str_begin and str_end
// std::string replace_from(std::string str, const std::string &new_word, std::string str_begin, std::string str_end)
// {
	// st pos_1 = str.find(str_begin);
	// st pos_2 = str.find(str_end);
	
	// if (pos_1 != npos && pos_2 != npos)
		// if (pos_1 > pos_2) 
		// {
			// std::swap(pos_1, pos_2);
			// str_begin.swap(str_end);
		// }
	
	// if (pos_1 != npos) pos_1 += str_begin.size();	// -1 +1
	// if (pos_2 != npos) pos_2 -= 1;					// 0 - 1 = npos
			
	// return replace_from(str, new_word, pos_1, pos_2);
// }


// std::string erase_d(std::string str, const std::string &new_word, std::string str_begin, std::string str_end)
// {
	

// }


int main()
{
	const std::string str("Some text 1 (Eng)"); 
	const std::string new_word("Tits");
	
	std::string result = replace_from(str, new_word, position(0, 3));
	print_str(result);
	result = replace_from(str, new_word, position('t', 'E', str));
	print_str(result);
	result = replace_from(str, new_word, position(0, '1', str));
	print_str(result);
	result = replace_from(str, new_word, position(3, 'd', str));
	print_str(result);
	
	
	// void (*out_pos)(const position)
	// auto out_pos = [](const position pos)
	// {
		// static int count = 0;
		// std::cout << "pos" << count << ' ' << pos << std::endl;
		// ++count;
	// };
	
	// position pos0(0, 10);
	// out_pos(pos0);
	// position pos1('s', 'n', "string");
	// out_pos(pos1);
	// position pos2(3, 't', "string");
	// out_pos(pos2);
	// position pos3('g', 2, "string");
	// out_pos(pos3);
	
	// position pos4('b', 4, "string");
	// out_pos(pos4);
	// position pos5(1, 'd', "string");
	// out_pos(pos5);
	
	// position pos6(static_cast<st>(90), static_cast<st>(100));
	// out_pos(pos6);
	
	
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