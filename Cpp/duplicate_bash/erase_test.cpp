#include <iostream>
#include <vector>
#include <algorithm>

int main()
{
	
	std::vector vec = {1,4,6,7,21,12,15,0,8};
	
	for (auto it = vec.begin(); it!= vec.end(); ++it)
	{
		std::cout << *it << std::endl;
		if (*it == 21 || *it == 4 || *it == 8 || *it == 1)
		{
			it = vec.erase(it);
			std::cout << "it after erase: " << *it << std::endl;
			--it;
		}
	}
	
	std::cout << std::endl;
	std::for_each(vec.begin(), vec.end(), [](const int &a)
	{
		std::cout << a << std::endl;
	});
	
	
	return 0;
}