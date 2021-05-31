#include <iostream>
#include <filesystem>
#include <string>
#include <vector>
#include <getopt.h>
//#include <cstring>	// strcpy
#include <algorithm>	// sort


namespace fs = std::filesystem;
using namespace std;

// globals
bool l_flag = false;
bool d_flag = false;
// bool q_flag = false;
int new_start = -1;
int new_end = -1;
fs::path dir;


bool is_num(const char ch)
{
	return 48 <= ch && ch <= 57;
}

bool is_num(const char * c_str)
{
	for (const char * ch = c_str; *ch != '\0'; ++ch )
	{
		if (!is_num(*ch)) {
			//std::cout << "is_num(" << *ch << ") = false" << endl;
			return false;
		}
		//else std::cout << "is_num(" << *ch << ") = true" << endl;
	}
	
	return true;
}

int parse(std::string str)
{
	std::string result;
	bool first_num = false;
	
	for (const char &ch : str)
	{
		if (is_num(ch))
		{
			result.push_back(ch);
			if (!first_num) first_num = true;
		}
		else if (first_num) break;
	}
	if (!result.empty()) return stoi(result);	// string
	else return -1;
}

int parse (const char * c_str)
{
	return parse(std::string(c_str));
}

// -p --path
void vec_init(vector<int> &vec, vector<int> &repeat)
{
	int val = 0;	// value
 
    for (fs::directory_entry const& entry : fs::directory_iterator(dir)) 
	{
        if (entry.is_regular_file()) 
		{
			if (entry.path().extension() == ".jpg" || entry.path().extension() == ".png")
			{
				val = parse(entry.path().stem().string());
				if (!vec.empty())
				{
					if (val != vec.back()) vec.push_back(val);
					else if (!d_flag) repeat.push_back(val);
				}
				else vec.push_back(val);
			}
        }
    }
	
	if (!vec.empty()) sort(vec.begin(), vec.end());
}

// start, end
void vec_run(vector<int> &vec, vector<int> &missing)
{
	using namespace std;
	if (!vec.empty())
	{
		int _start = vec.front();
		int _end = vec.back();
		auto iter = vec.begin();
		std::vector<int>::iterator result;
		
		if (new_start != -1)
		{
			if (new_start >= _start && new_start <= _end)
			{
				result = find(vec.begin(), vec.end(), new_start);
				if (result != vec.end())
				{
					iter = result;
					_start = new_start;
				}
				else
				{
					auto r_result = find_if(vec.rbegin(), vec.rend(), [](const int &a){return a < new_start;});
					if (r_result != vec.rend())
					{
						_start = *r_result;
						cout << "Start " << new_start << " is not availible. New start is " << *r_result << endl;
					}
				}
			}
			else cout << "Start value(" << new_start << ") must be bigger than a minimum value(" << _start << ')' <<
			" and smaller than a maximum value(" << _end << ')' << endl;
		}
		
		if (new_end != -1)
		{
			if (new_end >= _start && new_end <= _end)
				_end = new_end;
			else cout << "End value(" << new_end << ") must be bigger than a minimum value(" << _start << ')' <<
			" and smaller than a maximum value(" << _end << ')' << endl;
		}
		
		std::cout << "\nStart for a range " << _start << '-' << _end << std::endl;
		
		for (int i = _start; i <= _end; ++i)
		{
			if (i == *iter) iter++;
			else missing.push_back(i);
		}
	}
}

void test_getopt(int argc, char* argv[])
{
	using namespace std;
	
	int ch, value = 0;
	//++optind; // 3

	//opterr = 0;
	while ((ch = getopt(argc, argv, "-:qlhp:e:d")) != -1) {
		switch (ch) 
		{
		case 'p':	// path flag
			cout << "p flag active" << endl;
			if (optarg[0] == '-') 
			{
				cout << "Cannot use " << optarg << " as parameter for -" << (char)ch << endl;
				--optind;
			}
			else if (dir.empty())
			{
				fs::path temp_path(optarg);
				if (exists(temp_path)) dir = temp_path;
				else cout << "File path " << temp_path << " is not valid" << endl;
			}
			break;
		case 'e':	// end flag
			cout << "e flag active" << endl;
			if (optarg[0] == '-') 
			{
				cout << "Cannot use " << optarg << " as parameter for -" << (char)ch << endl;
				--optind;
			}
			else if (new_end == -1)
			{
				if (is_num(optarg))
				{
					new_end = parse(optarg);
					
					if (new_start > new_end)
						swap(new_start, new_end);
				}
				else cout << '\"' << optarg << "\": Invalid -" << (char)ch << " argument" << endl;
			}
			break;
		case 'l':	// oneline flag
			l_flag = true;
			cout << "l flag active" << endl;
			break;
		case 'd':	// duplicate files
			d_flag = true;
			cout << "d flag active" << endl;
			break;
		case 'h':	// help
			cout << "h --help flag active" << endl;
			break;
		case 'q':	// question flag
			cout << "q flag active" << endl;
			if (dir.empty()) dir = fs::current_path();
			break;
		case '?':
			cout << "\"-" << (char)optopt << "\": Invalid option" << endl;
			break;
		case 1:
			if (dir.empty())
			{
				fs::path temp_path(optarg);
				if (exists(temp_path)) dir = temp_path;
				else cout << "File path " << temp_path << " is not valid" << endl;
			}
			else if (is_num(optarg))
			{
				if (new_start == -1)
				{
					value = parse(optarg);
					if (value != -1) 
					{
						new_start = value;
					}
					else cout << '\"' << optarg << "\": Value cannot be a range START argument" << endl;
				} 
				else if (new_end == -1)
				{
					value = parse(optarg);
					if (value != -1) 
					{
						new_end = value;
						
						if (new_start > new_end)
						{
							// int temp = new_start;
							// new_start = new_end;
							// new_end = temp;
							swap(new_start, new_end);
						}
					}
					else cout << '\"' << optarg << "\": Value cannot be a range END argument" << endl;
				}
				else cout << '\"' << optarg << "\": Range arguments already present" << endl;
			} 
			else cout << '\"' << optarg << "\": Invalid value" << endl;
			break;
		default:
			/* none */
			break;
		}
	}
}

void check_path(int argc, char* argv[])
{
	using namespace std;
	
	if (dir.empty())
	{
		string answer;
		cout << "Do you want to use a current folder as a path? (y/n)" << endl;
		cout << "Use flag -q to avoid this question" << endl << ": ";
		cin >> answer;
		if (answer == "y" || answer == "yes") 
		{
			dir = fs::current_path();
		}
		else exit(0);
	}
	
	if (!exists(dir))
	{
		cout << "File path " << dir << " is not valid" << endl;
		exit(1);
	}
	//else cout << "Current path " << dir << endl;
}

int main(int argc, char* argv[])
{
    namespace fs = std::filesystem;
	using namespace std;
	typedef vector<int>::iterator it;
	
	vector<int> vec;
	vector<int> missing;
	vector<int> repeat;

	if (argc > 1) test_getopt(argc, argv);
	
	check_path(argc, argv);
	
	vec_init(vec, repeat);
	
	vec_run(vec, missing);
	
	string separator = "\n";
	if (l_flag) separator = ", ";
		
	if (!missing.empty())
	{
		it el;
		it penult = missing.end() - 1;
		cout << "\nMissing files is\n";
		for (el = missing.begin(); el != penult; ++el) 
		{
			cout << *el << separator;
		}
		cout << *el << endl;	// last
	}
	else cout << "\nNo missing files\n";

	if (!d_flag)
	if (!repeat.empty())
	{
		it el_r;
		it penult_r = repeat.end() - 1;
		cout << "\nDuplicate files is\n";
		for (el_r = repeat.begin(); el_r != penult_r; ++el_r) 
		{
			cout << *el_r << separator;
		}
		cout << *el_r << endl;	// last
	}
	
	// std::cin.get(); asdas
	
	return 0;
}