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
		// private
		position::assign(pos_1, pos_2);
	}
	
	position(st pos_1, st pos_2, const std::string &str)
	{
		// out of range check
		if (pos_1 > str.size()) pos_1 = 0;
		if (pos_2 > str.size()) pos_2 = 0;
		
		this->assign(pos_1, pos_2);
		// position::assign(pos_1, pos_2);
	}
	
	// position(int pos_1, int pos_2, const std::string &str) 
	// : position(static_cast<st>(pos_1), static_cast<st>(pos_2), str){}
	position(char ch_1, char ch_2, const std::string &str) : position(str.find(ch_1), str.find(ch_2), str){}
	position(int pos_1, char ch_2, const std::string &str) : position(static_cast<st>(pos_1), str.find(ch_2), str){}
	position(char ch_1, int pos_2, const std::string &str) : position(str.find(ch_1), static_cast<st>(pos_2), str){}
	
	// position between str_begin and str_end
	position(std::string str_begin, std::string str_end, const std::string &str)
	{
		st pos_1 = str.find(str_begin);
		st pos_2 = str.find(str_end);
		
		if (pos_1 != npos && pos_2 != npos)
		if (pos_1 > pos_2) 
		{
			position::swap(pos_1, pos_2);
			str_begin.swap(str_end);	// string swap
		}

		if (pos_1 != npos) pos_1 += str_begin.size();	// -1 +1
		if (pos_2 != npos) pos_2 -= 1;
		
		position::assign(pos_1, pos_2);
	}
	
	st get_pos1() const { return pos1;}
	st get_pos2() const { return pos2;}
	
	bool equal() const { return pos1 == pos2; }
	
private:

	void swap(st &pos_1, st &pos_2)
	{
		st temp = pos_1;
		pos_1 = pos_2;
		pos_2 = temp;
	}

	void assign(st pos_1, st pos_2)
	{
		if (pos_1 == npos && pos_2 == npos) { pos_1 = 0; pos_2 = 0;}
		else if (pos_1 == npos) pos_1 = pos_2;
		else if (pos_2 == npos) pos_2 = pos_1;
		else if (pos_1 > pos_2) position::swap(pos_1, pos_2);
		
		pos1 = pos_1;
		pos2 = pos_2;
	}
	
	//-----------------

	st pos1;
	st pos2;
};


std::ostream& operator<<(std::ostream &os, const position pos)
{
	os << pos.get_pos1() << ' ' <<  pos.get_pos2();
	return os;
}