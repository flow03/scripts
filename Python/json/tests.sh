python -u KEY_finder.py Mod_Text.d.json NAME_Bloodfly
echo "------------------------"
# python KEY_finder.py Mod_NPC_Names.d.json NpcName_Lena
# echo
# python KEY_finder.py Mod_NPC_Names.d.json NpcName_Alena
# echo

python -u KEY_finder.py
echo "------------------------"
python KEY_finder.py input.txt
echo "------------------------"
python KEY_finder.py empty.txt
echo "------------------------"
# python KEY_finder.py invalid_file.txt
# echo
python KEY_finder.py invalid_file.txt 1 2 3
# echo

# python KEY_finder.py Mod_Text.d.json NAME_Something
# echo
# python KEY_finder.py Text.d.json NAME_Bloodfly
# echo
# python KEY_finder.py None.json NAME_Bloodfly
# echo
# python KEY_finder.py None.json NAME_Something

# python read_file.py input.txt
# echo
# python read_file.py settings.txt
