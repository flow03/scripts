#include <iostream>
#include <filesystem>
#include <string>
#include <vector>
#include <getopt.h>
//#include <cstring>	// strcpy
#include <algorithm>	// sort, find, find_if


namespace fs = std::filesystem;
//using namespace std;

// globals
bool l_flag = false;
bool d_flag = false;
bool w_flag = false;
bool q_flag = false;
bool h_flag = false;
int new_start = -1;
int new_end = -1;
fs::path dir;
std::string new_ext = ".jpg";	// extension, e flag


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
	return parse(std::string(c_str));	// ???
}

// -p --path
void vec_init(std::vector<int> &vec, std::vector<int> &repeat)
{
	int val = 0;	// value
 
    for (fs::directory_entry const& entry : fs::directory_iterator(dir)) 
	{
        if (entry.is_regular_file())	//	|| entry.path().extension() == ".png"
		{
			std::cout << entry.path().filename().string();		// debug
			
			if (entry.path().extension() == ".jpg" || entry.path().extension() == ".png" || entry.path().extension() == new_ext)
			{	
				val = parse(entry.path().stem().string());
				
				if (!vec.empty())
				{
					if (val != vec.back()) vec.push_back(val);
					else if (d_flag) repeat.push_back(val);
				}
				else vec.push_back(val);
				std::cout << '*' << std::endl;		// debug
			} else std::cout << std::endl;			// debug
        }
    }
	
	if (!vec.empty()) sort(vec.begin(), vec.end());
}

// start, end
void vec_run(std::vector<int> &vec, std::vector<int> &missing)
{
	using namespace std;
	if (vec.size() > 2)
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
	else if (vec.empty()) cout << "\nNo numbered files in the current directory\n" << dir << endl;
	else if (vec.size() <= 2) cout << "\nNot enought arguments. " << vec.size() << " numbered files are in the directory\n" << dir << endl;
}

void test_getopt(int argc, char* argv[])
{
	using namespace std;
	
	int ch;
	//++optind; // 3

	//opterr = 0;
	while ((ch = getopt(argc, argv, "-:qlhp:b:dwe:")) != -1) {
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
		case 'b':	// back flag
			cout << "b flag active" << endl;
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
		case 'e':	// extension flag
			cout << "e flag active" << endl;
			if (optarg[0] == '-') 
			{
				cout << "Cannot use " << optarg << " as parameter for -" << (char)ch << endl;
				--optind;
			}
			else
			{
				new_ext = optarg;
				if (new_ext[0] != '.') new_ext = "." + new_ext; 
					//new_ext.insert(0, ".");
					//new_ext.push_front('.');
				cout << '\"' << new_ext << "\": is a new extension now" << endl;
			}
			break;
		case 'l':	// newline flag
			l_flag = true;
			cout << "l flag active" << endl;
			break;
		case 'd':	// duplicate files
			d_flag = true;
			cout << "d flag active" << endl;
			break;
		case 'w':	// window flag
			w_flag = true;
			cout << "w flag active" << endl;
			break;
		case 'h':	// help
			h_flag = true;
			cout << "h --help flag active" << endl;
			break;
		case 'q':	// question flag
			q_flag = true;
			cout << "q flag active" << endl;
			//if (dir.empty()) dir = fs::current_path();
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
				int value = 0;
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

bool check_path()
{
	using namespace std;
	bool result = true;
	
	if (dir.empty())
	{
		string answer;
		if (!q_flag)
		{
			cout << "Do you want to use a current folder as a path? (y/n)" << endl;
			cout << "Use flag -q to avoid this question" << endl << ": ";
			cin >> answer;
		}
		else answer = "y";
		
		if (answer == "y" || answer == "yes" || answer == "Y" || answer == "YES")
		{
			dir = fs::current_path();
		}
		else result = false;
	}
	
	if (!exists(dir))
	{
		cout << "File path " << dir << " is not valid" << endl;
		result = false;
	}
	//else cout << "Current path " << dir << endl;
	return result;
}

void vec_out(std::vector<int> &missing, std::vector<int> &repeat)
{
	using namespace std;
	typedef vector<int>::iterator it;
	
	string separator = ", ";
	if (l_flag) separator = "\n";
		
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

	if (d_flag)
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
}

void show_help()
{
	using std::cout;
	
	cout << "Create list of numbered files in directory and find missing numbers\n\n";
	cout << "miss_file [directory_path] [flags]\nmiss_file [flags] [directory_path]\n\n";
	cout << " -p\tmanually specify directory\n";
	cout << " -b\tmanually specify the last file\n";
	cout << " -e\tmanually specify extension, default work with jpg and png\n";
	cout << " -l\tcolumn output\n";
	cout << " -d\talso count duplicate numbers, may use with -l\n";
	cout << " -q\tdisable questions\n";
	cout << " -w\tdon't close console after(for Windows)\n";
	cout << " -h\tshow this help, discard other flags\n";
}

int main(int argc, char* argv[])
{
	using namespace std;
    namespace fs = std::filesystem;
	

	if (argc > 1) test_getopt(argc, argv);
	
	if (h_flag) show_help();
	else
	if (check_path())
	{
		vector<int> vec;
		vector<int> missing;
		vector<int> repeat;
	
		vec_init(vec, repeat);
		
		vec_run(vec, missing);
		
		vec_out(missing, repeat);
	}
	
	if (w_flag) std::cin.get();
	
	return 0;
}