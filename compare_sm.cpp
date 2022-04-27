#include <iostream>
#include <filesystem>
#include <string>
#include <vector>
#include <getopt.h>
//#include <cstring>	// strcpy
#include <algorithm>	// sort, find, find_if

namespace fs = std::filesystem;
typedef std::pair<fs::path, std::uintmax_t> couple_t;

fs::path dir_1;
fs::path dir_2;
fs::path dir_result;

bool e_flag = false;
// std::string compare_str;

#include "Compare.h"

cmp::ICompare * comparator = nullptr;

void check_dir(fs::path temp_path)
{
	if (exists(temp_path))
	{
		if (dir_1.empty()) dir_1 = temp_path;
		else if (dir_2.empty()) dir_2 = temp_path;
		//else if (dir_result.empty()) dir_result = temp_path;
	}
	else std::cout << "File path " << temp_path << " is not valid" << std::endl;
}

void test_getopt(int argc, char* argv[])
{
	using namespace std;
	
	int ch;
	
	while ((ch = getopt(argc, argv, "-:p:o:crte")) != -1) {
		switch (ch)
		{
		case 'p':	// path flag
			cout << "p flag active" << endl;
			if (optarg[0] == '-')
			{
				cout << "Cannot use " << optarg << " as parameter for -" << (char)ch << endl;
				--optind;
			}
			else check_dir(optarg);
			break;
		case 'c':	// copy flag
			if (!comparator)
			{
				comparator = new cmp::copy_compare();
				cout << "c flag active" << endl;
			}
			else cout << "\"-" << (char)ch << "\": Option " << comparator->name() << " compare already enabled" << endl;
			break;
		case 'r':	// replace flag
			if (!comparator)
			{
				comparator = new cmp::repl_compare();
				cout << "r flag active" << endl;
			}
			else cout << "\"-" << (char)ch << "\": Option " << comparator->name() << " compare already enabled" << endl;
			break;
		case 't':	// text flag
			if (!comparator)
			{
				comparator = new cmp::text_compare();
				cout << "t flag active" << endl;
			}
			else cout << "\"-" << (char)ch << "\": Option " << comparator->name() << " compare already enabled" << endl;
			break;
		case 'e':	// exterminate flag
			e_flag = true;
			cout << "e flag active" << endl;
			break;
		case 'o':	// out path flag
			cout << "o flag active" << endl;
			if (optarg[0] == '-') 
			{
				cout << "Cannot use " << optarg << " as parameter for -" << (char)ch << endl;
				--optind;
			}
			else if (fs::exists(optarg)) dir_result.assign(optarg);
			// try to create a new directory
			else if (fs::create_directory(optarg)) dir_result.assign(optarg);			// throw exception
			else std::cout << "File path " << optarg << " is not valid" << std::endl;	// never go here
			break;
		case '?':
			cout << "\"-" << (char)optopt << "\": Invalid option" << endl;
			break;
		case 1:
			check_dir(optarg);
			break;
		default:
			/* none */
			break;
		}
	}
}

std::vector<couple_t> vec_init(fs::path dir)
{
	std::vector<couple_t> folder;
	for (fs::directory_entry const& entry : fs::directory_iterator(dir)) 
	{
        if (entry.is_regular_file())
			folder.push_back(std::make_pair(entry.path(), entry.file_size()));
    }
	
	return folder;
}

// void vec_out(const std::vector<couple_t> &vec)
// {
	// for (const couple_t &el : vec)
		// std::cout << el.first.filename().string() << '\t' << el.second/1024 << " Kb" << std::endl;
// }

void compare(const std::vector<couple_t> &folder_1, const std::vector<couple_t> &folder_2)
{
	if (!comparator) comparator = new cmp::text_compare();	// as default
	
	if (comparator && comparator->name() != "text")
	{
		if (dir_result.empty())
		{
			fs::path temp_dir = dir_1/dir_1.filename() += "_result";
			std::string answer;
			std::string create_assign = "create";
			
			if (fs::exists(temp_dir)) create_assign = "assign";
			
			std::cout << "Would you like to " << create_assign << " a subdirectory " << temp_dir.string() << " as a result directory? (y/n) ";
				
			std::cin >> answer;
			if (answer == "y" || answer == "yes")
			{
				if (!fs::exists(temp_dir)) 
				{
					if (!fs::create_directory(temp_dir)) 
						std::cout << "Directory " << temp_dir.string() << " creation is failed" << std::endl;
				}
				else create_assign += "e";	// assign + e + d
				
				dir_result.assign(temp_dir);
				
				std::cout << "Directory " << temp_dir.string() << " is succefully " << create_assign << 'd' << std::endl;
			}
		}
	}
	
	if (!dir_result.empty() || comparator->name() == "text")
	{
		for (const couple_t &file_1 : folder_1)
		{
			for (const couple_t &file_2 : folder_2)
			{
				if (file_1.first.stem() == file_2.first.stem())	// filename without extension or stem
				{
					// pattern strategy
					comparator->compare(file_1, file_2);
					break;
				}
			}
		}
		
		delete comparator;
		std::cout << "Done!" << std::endl;
	}
	else std::cout << "Result directory is not specified" << std::endl;
}

int main(int argc, char* argv[])
{
	if (argc > 1) test_getopt(argc, argv);
	
	std::cout << "dir_1 : " << dir_1 << std::endl;
	std::cout << "dir_2 : " << dir_2 << std::endl;
	std::cout << "dir_result : " << dir_result << std::endl;
	std::cout << "sizeof(comparator) " << sizeof(comparator) << std::endl;
	std::cout << "sizeof(*comparator) " << sizeof(*comparator) << std::endl << std::endl;
	
	if (!dir_1.empty() && !dir_2.empty())
	{
		std::vector<couple_t> folder_1 = vec_init(dir_1);
		std::vector<couple_t> folder_2 = vec_init(dir_2);
		
		// comparison
		compare(folder_1, folder_2);
		
		// if (comparator->name() == "text")
			// comparator->_priv();
		
		if (e_flag)
		{
			std::string answer;
			std::cout << "Are you sure you want to delete the rest of contents of both folders? (y/n) ";
			std::cin >> answer;
			if (answer == "y" || answer == "yes") 
			{
				unsigned int count = 0;
				
				for (const couple_t &file : folder_1)
				if (exists(file.first)) 
				{
					fs::remove(file.first);
					++count;
				}
					
				for (const couple_t &file : folder_2)
				if (exists(file.first)) 
				{
					fs::remove(file.first);
					++count;
				}
				
				std::cout << count << " files was deleted" << std::endl;
			}
		}
	
	}
	else std::cout << "Not enough arguments to compare" << std::endl;
	
	return 0;
}