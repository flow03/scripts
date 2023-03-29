#include <iostream>
#include <vector>
#include <algorithm>
#include <iterator>	//ostream_iterator

void vec_out(const std::vector<int> &vec)
{
	for(const int &i : vec)
	{
		std::cout << i << ' ';
	}
	std::cout << std::endl; // << "size: " << vec.size() << std::endl;
}
void vec_out_it(const std::vector<int> &vec)
{
	std::copy(begin(vec), end(vec), std::ostream_iterator<int>(std::cout, " "));
	std::cout << std::endl;
}

int main()
{
	std::vector<int> vec = {1,4,6,7,0,6,12,0,21,12,15,0,8};
	std::cout << "vec:" << std::endl;
	vec_out(vec);
	
	std::sort(vec.begin(),vec.end());
	std::cout << "vec after sort:" << std::endl;
	vec_out_it(vec);
	
	auto u_it = std::unique(vec.begin(),vec.end());
	std::cout << "vec after unique:" << std::endl;
	vec_out(vec);
	std::cout << "u_it: " << *u_it << std::endl;
	
	std::vector<int> res;
	std::copy(u_it, vec.end(), std::back_inserter(res));
	std::cout << "res:" << std::endl;
	vec_out(res);
	
	return 0;
}
// g++ unique_test.cpp -o unique_test.exe -std=c++17
