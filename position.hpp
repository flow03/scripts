#pragma once
#include <string>

struct position
{
	typedef std::string::size_type st;
	// typedef std::string::npos npos;
	// using npos = std::string::npos;
	// #define npos std::string::npos
	
	position(st pos_1 = npos, st pos_2 = npos)
	{
		if (pos_1 != npos && pos_2 != npos)
		{
			if (pos_1 > pos_2) position::swap(pos_1, pos_2);
		}
		else if (pos_1 == npos) pos_1 = pos_2;
		else if (pos_2 == npos) pos_2 = pos_1;
		
		pos1 = pos_1;
		pos2 = pos_2;
	}
	
	// position(int pos_1, int pos_2) : position(pos_1, pos_2){}
	position(char ch_1, char ch_2, const std::string &str) : position(str.find(ch_1), str.find(ch_2)){}
	position(int pos_1, char ch_2, const std::string &str) : position(pos_1, str.find(ch_2)){}
	position(char ch_1, int pos_2, const std::string &str) : position(str.find(ch_1), pos_2){}
	
	st get_pos1() { return pos1;}
	st get_pos2() { return pos2;}
	
private:

	void swap(st &pos_1, st &pos_2)
	{
		st temp = pos_1;
		pos_1 = pos_2;
		pos_2 = temp;
	}
	
	st pos1;
	st pos2;
};


std::ostream& operator<<(std::ostream &os, position pos)
{
	os << pos.get_pos1() << ' ' <<  pos.get_pos2();
	return os;
}