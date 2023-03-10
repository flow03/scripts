#include <iostream>
#include <filesystem>
#include <string>
#include <vector>
#include <getopt.h>
//#include <cstring>	// strcpy
// #include <algorithm>	// sort, find, find_if

namespace fs = std::filesystem;
//typedef std::pair<fs::path, std::uintmax_t> couple_t;

fs::path dir_1;
// fs::path dir_2;
fs::path dir_result;

// bool e_flag = false;
// std::string compare_str;


void check_dir(fs::path temp_path)
{
	if (exists(temp_path))
	{
		if (dir_1.empty()) dir_1 = temp_path;
		// else if (dir_2.empty()) dir_2 = temp_path;
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
				// --optind;
			}
			else check_dir(optarg);
			break;
		// case 'c':	// copy flag
			// if (!comparator)
			// {
				// comparator = new cmp::copy_compare();
				// cout << "c flag active" << endl;
			// }
			// else cout << "\"-" << (char)ch << "\": Option " << comparator->name() << " compare already enabled" << endl;
			// break;
		// case 'r':	// replace flag
			// if (!comparator)
			// {
				// comparator = new cmp::repl_compare();
				// cout << "r flag active" << endl;
			// }
			// else cout << "\"-" << (char)ch << "\": Option " << comparator->name() << " compare already enabled" << endl;
			// break;
		// case 't':	// text flag
			// if (!comparator)
			// {
				// comparator = new cmp::text_compare();
				// cout << "t flag active" << endl;
			// }
			// else cout << "\"-" << (char)ch << "\": Option " << comparator->name() << " compare already enabled" << endl;
			// break;
		// case 'e':	// exterminate flag
			// e_flag = true;
			// cout << "e flag active" << endl;
			// break;
		/*case 'o':	// out path flag
			cout << "o flag active" << endl;
			if (optarg[0] == '-') 
			{
				cout << "Cannot use " << optarg << " as parameter for -" << (char)ch << endl;
				// --optind;
			}
			else if (fs::exists(optarg)) dir_result.assign(optarg);
			// try to create a new directory
			else if (fs::create_directory(optarg)) dir_result.assign(optarg);			// throw exception
			else std::cout << "File path " << optarg << " is not valid" << std::endl;	// never go here
			break;*/
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

// recursive
void vec_init(fs::path dir, std::vector<fs::path> &folder)
{
	for (fs::directory_entry const& entry : fs::directory_iterator(dir)) 
	{
        if (entry.is_regular_file())
			folder.push_back(entry.path());
		else if (entry.is_directory())
			vec_init(entry.path(), folder);	// recursive
    }
}

void vec_out(const std::vector<fs::path> &vec)
{
	//fs::path::preferred_separator = '/';
	
	for (const fs::path &el : vec)
		// std::cout << el.make_preferred().string() << std::endl; // non-const
		std::cout << el.generic_string() << std::endl; // separator '/' as default
		
	//std::cout << std::endl << vec.size() << " elements in container" << std::endl;
}

void vec_out(std::vector<std::vector<fs::path>> &dup)
{
	for (const std::vector<fs::path> &vec : dup)
	{
		vec_out(vec);
		std::cout << std::endl;
	}
}

bool comp_stem(const fs::path &path_1, const fs::path &path_2)
{
	return (path_1.stem() == path_2.stem());
}

bool comp_name(const fs::path &path_1, const fs::path &path_2)
{
	return (path_1.filename() == path_2.filename());
}

bool comp_size(const fs::path &path_1, const fs::path &path_2)
{
	return (file_size(path_1) == file_size(path_2));
}

std::vector<std::vector<fs::path>> vec_duplicate(std::vector<fs::path> vec)
{
	std::vector<std::vector<fs::path> > dup;
	std::vector<fs::path> res;
	
	for (auto it = vec.begin(); it!= vec.end(); ++it)
	{
		for (auto el = vec.begin(); el!= vec.end(); ++el)
		{
			if (el != it)
			{
				// change compare method
				if (comp_name(*el, *it))
				{
					if (res.empty()) res.push_back(*it);
					res.push_back(*el);
					vec.erase(el);
					--el;
				}
			}
		}
		vec.erase(it);
		--it;
		if (!res.empty())
		{
			dup.push_back(res);
			res.clear();
		}
	}
	
	return dup;
}


int main(int argc, char* argv[])
{
	if (argc > 1) test_getopt(argc, argv);
	
	std::cout << "dir_1 : " << dir_1 << std::endl;
	//std::cout << "dir_result : " << dir_result << std::endl;
	
	if (!dir_1.empty())
	{
		std::vector<fs::path> folder;
		vec_init(dir_1, folder);
		
		std::vector<std::vector<fs::path>> dup = vec_duplicate(folder);
		
		vec_out(dup);
		
		//vec_out(folder);
	}
	else std::cout << "Not enough arguments" << std::endl;
	
	return 0;
}

// ./duplicate_bash.exe -p ./test/pic1