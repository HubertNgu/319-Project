#!/bin/bash -xv

# This a script to automate pushing new changes to a branch onto origin
# This does not merge changes onto origin master

# To turn on DEBUG (printing only) type in echo
# Otherwise, leave this blank
# e.g. DEBUG=echo or DEBUG=
DEBUG=

# Parse the directory name
# In this case it would be the name of a team member
name=$(basename $PWD)

# Get the current time to mark the branch
# Using UNIX time
date=$(date "+%Y-%m-%d_%H-%M-%S")

$DEBUG git checkout -b $date-$name
$DEBUG git add .
$DEBUG git commit -am "Commiting work done by "$name
$DEBUG git checkout master
$DEBUG git pull origin
$DEBUG git checkout $date-$name
$DEBUG rm -rf .git/rebase-apply
$DEBUG git rebase master

# If the rebase failed (there were merge conflicts)
# then exit the program so that the user can deal
# with the merge conflicts before pushing their
# changes to the master repository
branch=$(git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/')

# Remove ( and ) in $branch and replace all spaces with -
# so we can do a simple string comparison
check_branch=${branch:1} # Remove leading space
check_branch=${check_branch//(/}
check_branch=${check_branch//)/}
check_branch=${check_branch// /-}

if [ $check_branch = "no-branch" ]
then
    echo
	echo ==================================================
	echo Failed to rebase your changes against the lastest
	echo changes in the master repository! You need to 
	echo manually merge your changes and then push your
	echo branch to the github repository. 
	echo The branch currently being rebased is:
	echo $date-$name
	echo ==================================================
    echo
    echo To fix this type the following commands into terminal
    echo 1. git status 
    echo "   - Make a note of what files have been MODIFIED"
    echo "   - Open each file that has been modified and manually fix conflicts"
    echo 2. git add .
    echo 3. git rebase --continue
    echo 4. git push origin $date-$name
    echo 5. git checkout master
	exit
fi

# Otherwise rebase must have been successful so
# push the new branch to github
echo Rebase against master was successful
