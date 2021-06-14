#include <iostream>
#include <filesystem>
#include <string>
#include <vector>
#include <getopt.h>
//#include <cstring>	// strcpy
#include <algorithm>	// sort, find, find_if


namespace fs = std::filesystem;
// using namespace std;

fs::path dir_1;
fs::path dir_2;
fs::path dir_result;

typedef std::pair<fs::path, std::uintmax_t> couple_t;

void check_dir(fs::path temp_path)
{
	if (exists(temp_path))
	{
		if (dir_1.empty()) dir_1 = temp_path;
		else if (dir_2.empty()) dir_2 = temp_path;
		else if (dir_result.empty()) dir_result = temp_path;
	}
	else std::cout << "File path " << temp_path << " is not valid" << std::endl;
}

void test_getopt(int argc, char* argv[])
{
	using namespace std;
	
	int ch;
	
	while ((ch = getopt(argc, argv, "-:p:r:")) != -1) {
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
		case 'r':	// result path flag
			cout << "r flag active" << endl;
			if (optarg[0] == '-') 
			{
				cout << "Cannot use " << optarg << " as parameter for -" << (char)ch << endl;
				--optind;
			}
			else if (fs::exists(optarg)) dir_result.assign(optarg);
			else std::cout << "File path " << optarg << " is not valid" << std::endl;
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

void vec_out(const std::vector<couple_t> &vec)
{
	for (const couple_t &el : vec)
		std::cout << el.first.filename().string() << '\t' << el.second/1024 << " Kb" << std::endl;
}

void compare(const std::vector<couple_t> &folder_1, const std::vector<couple_t> &folder_2)
{
	// auto lambda = [const &el](couple_t file){
		// return file.first == el.first;
	// };
	
	for (const couple_t &file_1 : folder_1)
		for (const couple_t &file_2 : folder_2)
		{
			if (file_1.first.filename() == file_2.first.filename())
			{
				if (file_1.second != file_2.second)
				{
					if (file_1.second < file_2.second)
					{
						std::cout << file_1.first.filename().string() << " from " << dir_1.filename() << " less than " << file_2.first.filename().string() << " from " << dir_2.filename() << " for " 
					<< (file_2.second - file_1.second)/1024 << " Kb" << std::endl;
					}
					else
					{
						std::cout << file_2.first.filename().string() << " from " << dir_2.filename() << " less than " << file_1.first.filename().string() << " from " << dir_1.filename() << " for " 
					<< (file_1.second - file_2.second)/1024 << " Kb" << std::endl;
					}
				}
				else 
					std::cout << "files " << file_1.first.filename().string() << " and " << file_2.first.filename().string() << " has equivalent size " << file_1.second/1024 << " Kb" << std::endl;
				break;
			}
		}
}

int main(int argc, char* argv[])
{
	if (argc > 1) test_getopt(argc, argv);
	
	std::cout << "dir_1 : " << dir_1 << std::endl;
	std::cout << "dir_2 : " << dir_2 << std::endl;
	// std::cout << "dir_2.parent_path() : " << dir_2.parent_path() << std::endl;
	// std::cout << "dir_2.generic_string() : " << dir_2.generic_string() << std::endl;
	if (dir_result.empty())
	{
		dir_result = fs::current_path();
		dir_result /= "dir_result";
		// fs::create_directory(dir_result);
	}
	std::cout << "dir_result : " << dir_result << std::endl;
	
	std::vector<couple_t> folder_1 = vec_init(dir_1);
	std::vector<couple_t> folder_2 = vec_init(dir_2);
	
	// std::cout << "\nfolder_1\n";
	// vec_out(folder_1);
	
	// std::cout << "\nfolder_2\n";
	// vec_out(folder_2);
	
	// comparison
	compare(folder_1, folder_2);
		
	// fs::path test("root/111/10/folder");
	// std::cout << "test.filename() : " << test.filename() << std::endl;
	
	std::cout << "Done!";
	
	return 0;
}