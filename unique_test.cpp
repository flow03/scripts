#include <iostream>
#include <vector>
#include <algorithm>

void vec_out(const std::vector<int> &vec)
{
	for(const int &i : vec)
	{
		std::cout << i << ' ';
	}
	std::cout << std::endl << "size: " << vec.size() << std::endl;
}

int main()
{
	std::vector<int> vec = {1,4,6,7,0,6,12,0,21,12,15,0,8};
	vec_out(vec);
	
	auto u_it = std::unique(vec.begin(),vec.end());
	vec_out(vec);
	std::cout << "u_it: " << *u_it;
	
	return 0;
}
// g++ unique_test.cpp -o unique_test.exe -std=c++17
