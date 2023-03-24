#include <iostream>
#include <filesystem>
#include <string>
#include <vector>
#include <getopt.h>
// #include <cstring>	// strcpy
// #include <algorithm>	// sort, find, find_if

#define _DEBUG
// #define sep fs::path::preferred_separator

namespace fs = std::filesystem;

fs::path dir_1;
// fs::path dir_2;
fs::path dir_result;

// bool e_flag = false;
// std::string compare_str;
struct flags
{
	flags()
	{
		c = false;
		r = false;
		t = false;
		n = false;
		s = false;
	}
	
	bool c, r, t, n, s;
};

void check_dir(fs::path temp_path)
{
	if (exists(temp_path))
	{
		if (dir_1.empty()) dir_1 = temp_path;
		// else if (dir_2.empty()) dir_2 = temp_path;
		// else if (dir_result.empty()) dir_result = temp_path;
	}
	else std::cout << "File path " << temp_path << " is not valid" << std::endl;
}

flags test_getopt(int argc, char* argv[])
{
	using namespace std;
	
	int ch;
	flags f;
	
	while ((ch = getopt(argc, argv, "-:p:o:crtns")) != -1) {
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
		case 'c':	// copy flag
			f.c = true;
			cout << "c flag active" << endl;
			break;
		case 'r':	// replace flag
			f.r = true;
			cout << "r flag active" << endl;
			break;
		case 't':	// text flag
			f.t = true;
			cout << "t flag active" << endl;
			break;
		case 'n':	// name flag
			f.n = true;
			cout << (char)ch << " flag active" << endl;
			break;
		case 's':	// size flag
			f.s = true;
			cout << (char)ch << " flag active" << endl;
			break;
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
		case '?':	// unknown flag
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
	
	return f;
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
					el = vec.erase(el);
					--el;
				}
			}
		}
		it = vec.erase(it);
		--it;
		if (!res.empty())
		{
			dup.push_back(res);
			res.clear();
		}
	}
	
	return dup;
}

std::vector<fs::path> unique_duplicate(std::vector<fs::path> vec, // by value
bool (*comp_method)(const fs::path&, const fs::path&) = &comp_name)
{
	std::vector<fs::path> u_res;
	#ifdef _DEBUG
	std::cout << "vec:\n";
	vec_out(vec);
	#endif
	
	auto u_it = std::unique(vec.begin(), vec.end(), comp_method);
	// auto u_it = std::unique(vec.begin(), vec.end());
	#ifdef _DEBUG
	std::cout << "\nvec after unique:\n";
	vec_out(vec);
	std::cout << "*u_it: "<<u_it->string() << std::endl;
	std::cout << "u_it == vec.end(): "<< (u_it == vec.end()) << std::endl;
	#endif
	
	// std::copy(u_it, vec.end(), std::back_inserter(u_res));
	// vec.erase(u_it, vec.end());
	vec.erase(vec.begin(), u_it);
	#ifdef _DEBUG
	std::cout << "\nu_res after erase:\n";
	vec_out(u_res);
	#endif
	
	return u_res;
}


// create new pathes with dir_result and rename the same filenames
// (need to rework)
std::vector<fs::path> vec_rename(const std::vector<fs::path> &vec)
{
	std::vector<fs::path> new_vec;
	fs::path new_path;
	std::string str_name;
	if (vec.size() > 1)
	{
		new_path = dir_result/vec.at(0).filename();
		new_vec.push_back(new_path);
		new_path.clear();
		// start on second element
		for (size_t i = 1; i < vec.size(); ++i)
		{
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
	// vec_out(new_vec);
	// std::cout << std::endl;
	#endif
	
	return new_vec;
}

// reworking
std::vector<fs::path> new_vec_rename(const std::vector<fs::path> &vec)
{
	std::vector<fs::path> new_vec;
	
	if (vec.size() > 1)
	{
		for (const fs::path &path : vec)
		{
			new_vec.push_back(dir_result/path.filename());
		}
		
		std::string str_name;
		
		// pointer realization
		size_t i = 0;	// counter
		for (auto cur = new_vec.begin(); cur != new_vec.end(); ++cur)	// current
		{
			i=0;
			for (auto sec = new_vec.begin(); sec != new_vec.end(); ++sec)	// second
			{
				if (cur!=sec)
				{
					if (cur->filename() == sec->filename())
					{
						str_name = sec->stem().string()+"_"+std::to_string(i)+sec->extension().string();	// counter using
						sec->replace_filename(str_name);	// replace_filename
						str_name.clear();
					}
				}
				++i;
			}
		}
	}
	else std::cout << "Invalid vector. Need two or more elements" << std::endl;
	
	#ifdef _DEBUG
	// vec_out(new_vec);
	// std::cout << std::endl;
	#endif
	
	return new_vec;
}

// copy files in one folder
void vec_copy(const std::vector<std::vector<fs::path>> &dup)
{
	std::vector<fs::path> new_names;
	// const auto copyOptions = fs::copy_options::skip_existing;
	#ifdef _DEBUG
	size_t count = 0;
	#endif
	for (const std::vector<fs::path> &vec : dup)
	{
		new_names = new_vec_rename(vec);
		if (vec.size() == new_names.size())
		{
			for (size_t i = 0; i < vec.size(); ++i)
			{
				if (!exists(new_names[i]))
				{
					fs::copy_file(vec[i], new_names[i], fs::copy_options::skip_existing);
					#ifdef _DEBUG
					++count;
					#endif
				}
				#ifdef _DEBUG
				else std::cout << new_names[i].string() << " already exists" << std::endl;
				#endif
			}
		} 
		else std::cout << "Invalid renamed vector size" << std::endl;
		#ifdef _DEBUG
		std::cout << count << " elements copied" << std::endl;
		count = 0;
		#endif
	}
}

int main(int argc, char* argv[])
{
	flags _flags;
	if (argc > 1) _flags = test_getopt(argc, argv);
	
	#ifdef _DEBUG
	// std::cout << "dir_1 : " << dir_1 << std::endl;
	// std::cout << "dir_result : " << dir_result << std::endl;
	#endif
	
	if (!dir_1.empty())
	{
		std::vector<fs::path> folder;
		vec_init(dir_1, folder);
		
		bool (*comp_method)(const fs::path&, const fs::path&) = &comp_name;
		if (_flags.s) 
		{
			comp_method = &comp_size;
			#ifdef _DEBUG
			std::cout<<"comp_method comp_size"<<std::endl;
			#endif
		}
		
		// std::cout<<"vec_duplicate:"<<std::endl;
		// std::vector<std::vector<fs::path>> dup = vec_duplicate(folder, comp_method);
		// vec_out(dup);
		
		std::vector<fs::path> u_dup = unique_duplicate(folder, comp_method);
		// std::cout<<"unique_duplicate:"<<std::endl;
		// vec_out(u_dup);
		
		#ifdef _DEBUG
		// std::cout<<"Vec_replace and _rename:"<<std::endl;
		#endif
		// vec_copy(dup);
		
		//vec_out(folder);
	}
	else std::cout << "Not enough arguments" << std::endl;
	
	return 0;
}

// ./duplicate_bash.exe -p ./test/pic1
// ./duplicate_bash.exe -p ./test/dup -o ./test/dup_result
