#include <iostream>
#include <string>		// C++ style - find, substr, replace, length, size, npos
#include <algorithm>	// swap

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
void print(std::string::size_type pos, std::string const &s, std::string::size_type count = std::string::npos)
{
    if (pos == std::string::npos) 
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
	if (pos != std::string::npos) 
		result_str = str.replace(pos, word.size(), new_word);
	
	return result_str;	// returns empty string if failed
}

// replace text start with pos_1 to pos_2 inclusive
std::string replace_from(std::string str, const std::string &new_word, 
std::string::size_type pos_1 = std::string::npos, 
std::string::size_type pos_2 = std::string::npos)
{
	std::string result_str;
	
	if (pos_1 == std::string::npos) pos_1 = 0;
	if (pos_2 == std::string::npos) pos_2 = str.size() - 1;
	if (pos_1 > pos_2) std::swap(pos_1, pos_2);
	
	// std::string::const_iterator ipos_1 = str.begin() + pos_1;
	// std::string::const_iterator ipos_2 = str.begin() + pos_2 + 1;
	// result_str = str.replace(ipos_1, ipos_2, new_word);
	
	result_str = str.replace(pos_1, (pos_2 - pos_1 + 1), new_word);
	
	
	return result_str;
}

// replace text between str_begin and str_end
std::string replace_from(std::string str, const std::string &new_word, std::string str_begin, std::string str_end)
{
	std::string::size_type pos_1 = str.find(str_begin);
	std::string::size_type pos_2 = str.find(str_end);
	
	if (pos_1 != std::string::npos && pos_2 != std::string::npos)
		if (pos_1 > pos_2) 
		{
			std::swap(pos_1, pos_2);
			// std::swap(str_begin, str_end);
			str_begin.swap(str_end);
		}
	
	if (pos_1 != std::string::npos) pos_1 += str_begin.size(); // -1 +1
	if (pos_2 != std::string::npos) pos_2 -= 1;
			
	return replace_from(str, new_word, pos_1, pos_2);
}


int main()
{
	std::string::size_type pos;
	std::string str("Some string 1 (Eng)");
	std::string str_repl("Huge Boobs");
	std::string new_str;
	
	std::cout << str << std::endl << std::endl;


	new_str = replace_with(str, "Eng" , str_repl);
	print_str(new_str);
	new_str = replace_with(str, "string" , str_repl);
	print_str(new_str);
	new_str = replace_from(str, str_repl, 5);
	print_str(new_str);
	new_str = replace_from(str, str_repl, 3, 0);
	print_str(new_str);
	new_str = replace_from(str, str_repl, "Some ", "(Eng)");
	print_str(new_str);
	new_str = replace_from(str, str_repl, "(Eng)", "Some ");
	print_str(new_str);
	
	
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