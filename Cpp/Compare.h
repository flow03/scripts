// #pragma once

#include <string>
//#include <filesystem>

//namespace fs = std::filesystem;
//typedef std::pair<fs::path, std::uintmax_t> couple_t;

namespace cmp
{
	
struct ICompare
{
	virtual void compare(const couple_t &file_1, const couple_t &file_2) = 0;
	virtual ~ICompare() = default;
	virtual std::string name() = 0;
	
	// 0 - equal, 1 - bigger, 2 - smaller
	int compare_and_out(const couple_t &file_1, const couple_t &file_2)
	{
		int result = 0;
		
		if (file_1.second != file_2.second)
		{
			if (file_1.second > file_2.second)
			{
				diff = (file_1.second - file_2.second)/1024;
				p_color1 = green;
				p_color2 = red;
				result = 1;
			}
			else
			{
				diff = (file_2.second - file_1.second)/1024;
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
	
	private:
	const std::string red = "\033[0;31m";
	const std::string green = "\033[0;32m";
	const std::string white = "\033[0;37m";
	const std::string reset = "\033[0m";
	std::string p_color1;
	std::string p_color2;
	std::uintmax_t diff;
};

struct text_compare : public ICompare
{
	// text_compare() = default;
	void compare(const couple_t &file_1, const couple_t &file_2) override
	{
		compare_and_out(file_1, file_2);
	}
	
	std::string name(){return "text";}
	
	// void call_private(){ICompare::_priv();}
};

struct copy_compare : public ICompare
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

struct repl_compare : public ICompare	// replace
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
				out_str = "Renamed " + file_2.first.string() + " " + to_string(difference) + " Kb";
				rename_path = file_2.first;
				result_path = dir_result/file_2.first.filename();	// operator/ preferred separator
			}
			else
			{
				difference = ((intmax_t)file_2.second - file_1.second)/1024;
				out_str = "Renamed " + file_1.first.string() + " " + to_string(difference) + " Kb";
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