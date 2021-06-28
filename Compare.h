// #pragma once

namespace cmp
{
	
struct ICompare
{
	virtual void compare(const couple_t &file_1, const couple_t &file_2) = 0;
	virtual ~ICompare() = default;
	virtual std::string name() = 0;
};

struct text_compare : ICompare
{
	// text_compare() = default;
	void compare(const couple_t &file_1, const couple_t &file_2) override
	{
		if (file_1.second != file_2.second)
		{
			if (file_1.second < file_2.second)
			{
				std::cout << file_1.first.filename().string() << " from " << dir_1.filename() << " less than " << file_2.first.filename().string() << " from " << dir_2.filename() << " for " << (file_2.second - file_1.second)/1024 << " Kb" << std::endl;
			}
			else
			{
				std::cout << file_2.first.filename().string() << " from " << dir_2.filename() << " less than " << file_1.first.filename().string() << " from " << dir_1.filename() << " for " << (file_1.second - file_2.second)/1024 << " Kb" << std::endl;
			}
		}
		else std::cout << "files " << file_1.first.filename().string() << " and " << file_2.first.filename().string() << " has equivalent size " << file_1.second/1024 << " Kb" << std::endl;
	}
	
	std::string name(){return "text";}
};

struct copy_compare : ICompare
{
	void compare(const couple_t &file_1, const couple_t &file_2) override
	{
	if (!dir_result.empty())
	{
		if (file_1.second != file_2.second)
		{
			const auto copyOptions = fs::copy_options::skip_existing; // | fs::copy_options::skip_symlinks;
			
			if (file_1.second < file_2.second)
			{
				if (!fs::exists(dir_result/file_1.first.filename()))
				{
					fs::copy_file(file_1.first, dir_result/file_1.first.filename(), copyOptions);	// operator/ preferred separator
					std::cout << file_1.first.filename().string() << " copied from " << file_1.first.parent_path().string() << "\t" << (file_2.second - file_1.second)/1024 << " Kb" 
					<< std::endl;
				}
				else std::cout << "The file " << (dir_result/file_1.first.filename()).string() << " already exists" << std::endl;
			}
			else
			{
				if (!fs::exists(dir_result/file_2.first.filename()))
				{
					fs::copy_file(file_2.first, dir_result/file_2.first.filename(), copyOptions);
					std::cout << file_2.first.filename().string() << " copied from " << file_2.first.parent_path().string() << "\t" << (file_1.second - file_2.second)/1024 << " Kb" 
					<< std::endl;
				}
				else std::cout << "The file " << (dir_result/file_2.first.filename()).string() << " already exists" << std::endl;
			}
		}
		else std::cout << "Equivalent files " << file_1.first.filename().string() << " and " << file_2.first.filename().string() 
		<< "\t" << file_2.second/1024 << " Kb" << std::endl;
	}
	else std::cout << "Result directory invalid. Use parameter -o with argument to set result directory" << std::endl;
	}
	
	std::string name(){return "copy";}
};

struct repl_compare : ICompare	// replace
{
	void compare(const couple_t &file_1, const couple_t &file_2) override
	{
	using namespace std;
	if (!dir_result.empty())
	{
		std::intmax_t difference;	// signed
		fs::path rename_path;
		fs::path result_path;
		std::string out_str;		// out result string
		
		if (file_1.second != file_2.second)
		{
			if (file_2.second < file_1.second) //  + (100 * 1024)
			{
				difference = ((intmax_t)file_1.second - file_2.second)/1024;
				out_str = "Renamed " + file_2.first.string() + " " + to_string(difference) + " Kb diff";
				rename_path = file_2.first;
				result_path = dir_result/file_2.first.filename();	// operator/ preferred separator
			}
			else
			{
				difference = ((intmax_t)file_2.second - file_1.second)/1024;
				out_str = "Renamed " + file_1.first.string() + " " + to_string(difference) + " Kb diff";
				rename_path = file_1.first;
				result_path = dir_result/file_1.first.filename();
			}
			
			if (!fs::exists(result_path))
			{	
				fs::rename(rename_path, result_path);
				std::cout << out_str << std::endl;
			}
			else std::cout << "File " << result_path.string() << " already exists" << std::endl;
		}
		else std::cout << "Equivalent files " << file_1.first.filename().string() << " and " << file_2.first.filename().string()
			<< "\t" << file_2.second/1024 << " Kb" << std::endl;
	}
	else std::cout << "Result directory invalid. Use parameter -o with argument to set result directory" << std::endl;
	}
	
	std::string name(){return "rename";}
};

}