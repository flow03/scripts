#include <iostream>
#include <filesystem>
#include <string>
#include <vector>
#include <getopt.h>
// #include <cstring>	// strcpy
// #include <algorithm>	// sort, find, find_if

#define _DEBUG
#define sep fs::path::preferred_separator

namespace fs = std::filesystem;

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
			#ifdef _DEBUG
			cout << "p flag active" << endl;
			#endif
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
		case 'o':	// out path flag
			#ifdef _DEBUG
			cout << "o flag active" << endl;
			#endif
			if (optarg[0] == '-') 
			{
				cout << "Cannot use the " << optarg << " as parameter for -" << (char)ch << endl;
				// --optind;
			}
			else if (fs::exists(optarg)) dir_result.assign(optarg);
			// try to create a new directory
			else cout << "Cannot use the " << optarg << " as result directory. It does not exist" << endl;
			//else if (fs::create_directory(optarg)) dir_result.assign(optarg);			// throw exception
			//else std::cout << "File path " << optarg << " is not valid" << std::endl;	// never go here
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

void vec_out(const std::vector<std::vector<fs::path>> &dup)
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

// bool (*comp_method)(const fs::path&, const fs::path&) = &comp_name;
// auto comp_method = &comp_name;

std::vector<std::vector<fs::path>> vec_duplicate(std::vector<fs::path> vec, 
bool (*comp_method)(const fs::path&, const fs::path&) = &comp_name)
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
				if (comp_method(*el, *it))
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

// create new pathes with dir_result and rename the same filenames
std::vector<fs::path> _rename(const std::vector<fs::path> &vec)
{
	std::vector<fs::path> new_vec;
	fs::path new_path;
	std::string str_name;
	if (vec.size() > 1)
	{
		new_path = dir_result/vec.at(0).filename();
		new_vec.push_back(new_path);
		for (size_t i = 1; i < vec.size(); ++i)
		{
			new_path.clear();
			if (vec[i].filename() == vec[0].filename())
			{
				// str = "_"+std::to_string(i);
				// new_path = (((dir_result/="replaced")/=vec[i].stem())+=str)+=vec[i].extension();
				str_name = vec[i].stem().string()+"_"+std::to_string(i)+vec[i].extension().string();
				new_path = dir_result/str_name;
				str_name.clear();
			}
			else new_path = dir_result/vec[i].filename();
			
			// std::cout << new_path.string() << std::endl;
			new_vec.push_back(new_path);
			new_path.clear();
		}
	}
	
	#ifdef _DEBUG
	vec_out(new_vec);
	std::cout << std::endl;
	#endif
	
	return new_vec;
}

void vec_replace(const std::vector<std::vector<fs::path>> &dup)
{
	for (auto vec = dup.begin(); vec!= dup.end(); ++vec)
	{
		_rename(*vec);
	}
}

int main(int argc, char* argv[])
{
	if (argc > 1) test_getopt(argc, argv);
	
	#ifdef _DEBUG
	std::cout << "dir_1 : " << dir_1 << std::endl;
	std::cout << "dir_result : " << dir_result << std::endl;
	#endif
	
	if (!dir_1.empty())
	{
		std::vector<fs::path> folder;
		vec_init(dir_1, folder);
		
		bool (*comp_method)(const fs::path&, const fs::path&) = &comp_name;
		
		
		std::vector<std::vector<fs::path>> dup = vec_duplicate(folder, comp_method);
		
		vec_out(dup);
		
		#ifdef _DEBUG
		std::cout<<"vec_replace and _rename:"<<std::endl;
		#endif
		vec_replace(dup);
		
		//vec_out(folder);
	}
	else std::cout << "Not enough arguments" << std::endl;
	
	return 0;
}

// ./duplicate_bash.exe -p ./test/pic1
// ./duplicate_bash.exe -p ./test/dup -o ./test/dup_result
