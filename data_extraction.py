import sys
import os
import re
from BeautifulSoup import BeautifulSoup

def write_meal_to_files(meal, meal_totals, outfile, meal_file, all_food_file, meal_totals_file, meal_name, date):
    
    outfile.write('%s,Calories,Carbs,Fat,Protein,Sugar,Iron\n' % meal_name)
    for food, values in meal.iteritems():
        name = re.sub(',', '-', food).encode('utf-8')
        meal_file.write('%s,%s,' % (date, name))
        all_food_file.write('%s,%s,' % (date,name))
        outfile.write('%s,' % name)
        for val in values:
            if val == '&nbsp;':
                val = '0'
            meal_file.write('%s,' % re.sub(',', '', val))
            all_food_file.write('%s,' % re.sub(',', '', val))
            outfile.write('%s,' % re.sub(',', '', val))
        meal_file.write('\n')
        all_food_file.write('\n')
        outfile.write('\n')

        meal_file.flush()
        all_food_file.flush()
        outfile.flush()

    outfile.write('%s Total,' % meal_name)
    meal_totals_file.write('%s,' % date)
    for val in meal_totals:
        if val == '&nbsp;':
            val = '0'
        outfile.write('%s,' % re.sub(',', '', val))
        meal_totals_file.write('%s,' % re.sub(',', '', val))
    outfile.write('\n')
    meal_totals_file.write('\n')

    outfile.flush()
    meal_totals_file.flush()


def extract_data(username):

    cwd = os.getcwd()
    food_dir = os.path.join(username, 'food')
    food_path = os.path.join(cwd, food_dir)
    exer_dir = os.path.join(username, 'exercise')
    exercise_path = os.path.join(cwd, exer_dir)
    csv_dir = os.path.join(username, 'csv')
    csv_path = os.path.join(cwd, csv_dir)
    plot_dir = os.path.join(username, 'plot')
    plot_path = os.path.join(cwd, plot_dir)

    if not os.path.isdir(csv_path):
        os.mkdir(csv_path)
    if not os.path.isdir(plot_path):
        os.mkdir(plot_path)



    exercise_files = os.listdir(exercise_path)

    cardio_file = open(os.path.join(csv_path, 'cardio_exercise.csv'), 'w')
    cardio_file.write('Date,Exercise,Minutes,Calories\n')
    strength_file = open(os.path.join(csv_path, 'strength_exercise.csv'), 'w')
    strength_file.write('Date,Exercise,Sets,Reps per Set,Weight per Set\n')
    cardio_totals_file = open(os.path.join(csv_path, 'cardio_totals.csv'), 'w')
    cardio_totals_file.write('Date,Daily Total (Minutes), Daily Total (Calories), Weekly Total (Minutes), Weekly Total (Calories)\n')
    for file in exercise_files:
        if '.html' in file:
            cardio, strength, totals = extract_exercise_data(os.path.join(exercise_path, file))
            date = file.lstrip('exercise_diary_').rstrip('.html')
            print date
            outfile = open(os.path.join(csv_path, file.rstrip('.html') + '.csv'), 'w')
        
            daily_total = totals[0]
            daily_goal = totals[1]
            weekly_total = totals[2]
            weekly_goal = totals[3]      

            outfile.write('Exercise,Minutes,Calories\n')
            for ex in cardio:
                name = ex[0]
                name = re.sub(',', '-', name)
                outfile.write(u'%s,%s,%s\n' % (name, ex[1], ex[2]))
                cardio_file.write('%s,%s,%s,%s\n' % (date, name, ex[1], ex[2]))

            outfile.write('\n')
            outfile.write('Daily Total (Minutes), Daily Goal (Minutes)\n')
            outfile.write('%s,%s\n' % (daily_total[0], daily_goal[0]))
            outfile.write('\n')
            outfile.write('Daily Total (Calories), Daily Goal (Calories)\n')
            outfile.write('%s,%s\n' % (daily_total[1], daily_goal[1]))
            outfile.write('\n')
            outfile.write('Weekly Total (Minutes), Weekly Goal (Minutes)\n')
            outfile.write('%s,%s\n' % (weekly_total[0], weekly_goal[0]))
            outfile.write('\n')
            outfile.write('Weekly Total (Calories), Weekly Goal (Calories)\n')
            outfile.write('%s,%s\n' % (weekly_total[1], weekly_goal[1]))
            outfile.write('\n')
            outfile.write('Exercise,Sets,Reps per Set, Weight per Set\n')
            cardio_totals_file.write('%s,%s,%s,%s,%s\n' % (date, daily_total[0], daily_total[1], weekly_total[0], weekly_total[1]))

            for ex in strength:
                name = ex[0]
                name = re.sub(',', '-', name)
                outfile.write('%s,%s,%s,%s\n' % (name, ex[1], ex[2], ex[3]))
                strength_file.write('%s,%s,%s,%s,%s\n' % (date, name, ex[1], ex[2], ex[3]))

    food_files = os.listdir(food_path)

    all_food_file = open(os.path.join(csv_path, 'all_food.csv'), 'w')
    all_food_file.write('Date,Food,Calories,Carbs,Fat,Protein,Sugar,Iron\n')
    breakfast_file = open(os.path.join(csv_path, 'breakfast_food.csv'), 'w')
    breakfast_file.write('Date,Food,Calories,Carbs,Fat,Protein,Sugar,Iron\n')
    breakfast_totals_file = open(os.path.join(csv_path, 'breakfast_totals.csv'), 'w')
    breakfast_totals_file.write('Date,Calories,Carbs,Fat,Protein,Sugar,Iron\n')
    midmorning_file = open(os.path.join(csv_path, 'breakfast_food.csv'), 'w')
    midmorning_file.write('Date,Food,Calories,Carbs,Fat,Protein,Sugar,Iron\n')
    midmorning_totals_file = open(os.path.join(csv_path, 'breakfast_totals.csv'), 'w')
    midmorning_totals_file.write('Date,Calories,Carbs,Fat,Protein,Sugar,Iron\n')
    lunch_file = open(os.path.join(csv_path, 'lunch_food.csv'), 'w')
    lunch_file.write('Date,Food,Calories,Carbs,Fat,Protein,Sugar,Iron\n')
    lunch_totals_file = open(os.path.join(csv_path, 'lunch_totals.csv'), 'w')
    lunch_totals_file.write('Date,Calories,Carbs,Fat,Protein,Sugar,Iron\n')
    midafternoon_file = open(os.path.join(csv_path, 'breakfast_food.csv'), 'w')
    midafternoon_file.write('Date,Food,Calories,Carbs,Fat,Protein,Sugar,Iron\n')
    midafternoon_totals_file = open(os.path.join(csv_path, 'breakfast_totals.csv'), 'w')
    midafternoon_totals_file.write('Date,Calories,Carbs,Fat,Protein,Sugar,Iron\n')
    dinner_file = open(os.path.join(csv_path, 'dinner_food.csv'), 'w')
    dinner_file.write('Date,Food,Calories,Carbs,Fat,Protein,Sugar,Iron\n')
    dinner_totals_file = open(os.path.join(csv_path, 'dinner_totals.csv'), 'w')
    dinner_totals_file.write('Date,Calories,Carbs,Fat,Protein,Sugar,Iron\n')
    evening_file = open(os.path.join(csv_path, 'snacks_food.csv'), 'w')
    evening_file.write('Date,Food,Calories,Carbs,Fat,Protein,Sugar,Iron\n')
    evening_totals_file = open(os.path.join(csv_path, 'snacks_totals.csv'), 'w')
    evening_totals_file.write('Date,Calories,Carbs,Fat,Protein,Sugar,Iron\n')
    totals_file = open(os.path.join(csv_path, 'food_totals.csv'), 'w')
    totals_file.write(',Calories,Calories,Calories,Carbs,Carbs,Carbs,Fat,Fat,Fat,Protein,Protein,Protein,Sugar,Sugar,Sugar,Iron,Iron,Iron\n')
    totals_file.write('Date,Total,Goal,Remaining,Total,Goal,Remaining,Total,Goal,Remaining,Total,Goal,Remaining,Total,Goal,Remaining,Total,Goal,Remaining\n')

    for file in food_files:
        if '.html' in file:
            data, meal_total, total = extract_food_data(os.path.join(food_path, file))
            date = file.lstrip('food_diary_').rstrip('.html')
            print date
            outfile = open(os.path.join(csv_path, file.rstrip('.html') + '.csv'), 'w')

            breakfast = data['Breakfast']
            breakfast_totals = meal_total['Breakfast']
            write_meal_to_files(breakfast, breakfast_totals, outfile, 
                            breakfast_file, all_food_file, breakfast_totals_file, 'Breakfast', date)

            midmorning = data['Mid Morning']
            midmorning_totals = meal_total['Mid Morning']
            write_meal_to_files(midmorning, midmorning_totals, outfile, 
                            midmorning_file, all_food_file, midmorning_totals_file, 'Mid Morning', date)

            lunch = data['Lunch']
            lunch_totals = meal_total['Lunch']
            write_meal_to_files(lunch, lunch_totals, outfile, 
                            lunch_file, all_food_file, lunch_totals_file, 'Lunch', date)

            midafternoon = data['Mid Afternoon']
            midafternoon_totals = meal_total['Mid Afternoon']
            write_meal_to_files(midafternoon, midafternoon_totals, outfile, 
                            midafternoon_file, all_food_file, midafternoon_totals_file, 'Mid Afternoon', date)
            
            dinner = data['Dinner']
            dinner_totals = meal_total['Dinner']
            write_meal_to_files(dinner, dinner_totals, outfile, 
                            dinner_file, all_food_file, dinner_totals_file, 'Dinner', date)

            evening = data['Evening']
            evening_totals = meal_total['Evening']
            write_meal_to_files(evening, evening_totals, outfile, 
                            evening_file, all_food_file, evening_totals_file, 'Evening', date)

            totals = total['Totals']
            remaining = total['Remaining']
            goal = total['Your Daily Goal']

            totals_file.write('%s' % date)
            for i in range(0,len(totals)):
                t = re.sub(',', '', totals[i])
                if t == '&nbsp;':
                    t = '0'
                g = re.sub(',', '', goal[i])
                if g == '&nbsp;':
                    g = '0'
                r = re.sub(',', '', remaining[i])
                if r == '&nbsp;':
                    g = '0'
                totals_file.write(',%s,%s,%s' % (t,g,r))
            totals_file.write('\n')

def extract_exercise_data(file):
    cardio = []
    strength = []
    daily_total = []
    weekly_total = []
    daily_goal = []
    weekly_goal = []

    html = open(file, 'r').read()
    soup = BeautifulSoup(html)

    result = soup.find('span', 'date')
    date = result.contents[2].strip()

    # two tables in exercise data, cardio and strength
    tables = soup.findAll('table', 'table0')

    # go through both tables
    for table in tables:
        # remove a bunch of crap we definitely don't want
        quick_tools = table.findAll('div', 'quick_tools')
        thead = table.findAll('thead')
        delete = table.findAll('td', {'class' : 'delete'})
        [qt.extract() for qt in quick_tools]
        [t.extract() for t in thead]
        [d.extract() for d in delete]

    #go through both tables
    for table in tables:
        # cardio exercise table
        if table.get('id') == 'cardio-diary':
            # get all the rows
            rows = table.findAll('tr')
            for row in rows:
                # if no class, is an exercise
                if row.get('class') is None:
                    # get the cells
                    cells = row.findAll('td')
                    # no span in cells, is definitely an exercise
                    if cells[0].find('span') is None:
                        # get exercise description
                        name = cells[0].contents[1].contents[0].strip()
                        c = []
                        c.append(name)
                        # get values for exercise
                        for cell in cells[1:]:
                            if cell.find('span') is None:
                                if not cell.get('class') == 'empty':
                                    c.append(cell.contents[0].strip())
                        # add to the list
                        cardio.append(c)
                    # span in cells, is total values
                    else:
                        # rows containing spans are totals
                        totals = row.findAll('span')
                        if totals[0].contents[0].strip() == 'Daily Total /':
                            for i in range(2, len(totals), 2):
                                daily_total.append(totals[i].contents[0].strip())
                                daily_goal.append(totals[i+1].contents[0].strip())
                        if totals[0].contents[0].strip() == 'Weekly Total /':
                            for i in range(2, len(totals), 2):
                                weekly_total.append(totals[i].contents[0].strip())
                                weekly_goal.append(totals[i+1].contents[0].strip())

        # other table is strength training
        else:
            # get all the rows
            rows = table.findAll('tr')
            for row in rows:
                # if no class, is an exercise
                if row.get('class') is None:
                    c = []
                    cells = row.findAll('td')
                    # get the exercise name
                    name = cells[0].contents[1].contents[0].strip()
                    c.append(name)
                    for cell in cells[1:]:
                        c.append(cell.contents[0].strip())
                    strength.append(c)

    totals = [daily_total, daily_goal, weekly_total, weekly_goal]
    return cardio, strength, totals

def extract_food_data(file):
    data = {}
    meal_total = {}
    total = {}
    # open the file and read the html into Beautiful Soup
    html = open(file, 'r').read()
    soup = BeautifulSoup(html)

    # get the date of the diary entry
    result =  soup.find('span',  'date')
    date = result.contents[2].strip()

    # find the main data table
    table = soup.find('table', 'table0')
    
    # the quick_tools stuff is just annoying, so get rid of it so 
    # we have a clean table to work with
    quick_tools = table.findAll('div', 'quick_tools')
    [qt.extract() for qt in quick_tools]

    # get all the rows in the table
    rows = table.findAll('tr')
    current_meal = None
    for row in rows:
        # meal header row gives us current meal
        if row.get('class') == 'meal_header':
            cells = row.findAll('td')
            # cell 0 contains meal name
            current_meal = cells[0].contents[0].strip()
            # make sure we have somewhere to store data
            if data.get(current_meal) is None:
                data[current_meal] = {}
            if meal_total.get(current_meal) is None:
                meal_total[current_meal] = []
        # bottom row has totals for current meal
        if row.get('class') == 'bottom':
            cells = row.findAll('td')
            # data is from cell 1 onwards
            for cell in cells[1:]:
                meal_total[current_meal].append(cell.contents[0].strip())
        # no class means a food item is in the row
        if row.get('class') is None:
            cells = row.findAll('td')
            # first alt cell contains name of the food
            if cells[0].get('class') == 'first alt':
                name = cells[0].contents[1].contents[0].strip()
                # list to store attributes
                data[current_meal][name] = []
                # extract attributes
                for cell in cells[1:]:
                    data[current_meal][name].append(cell.contents[0].strip())
        # total rows
        if row.get('class') in ['total','total alt','total remaining']:
            # get cells
            cells = row.findAll('td')
            # first cell has name of total
            name = cells[0].string.strip()
            # fill the remaining values
            total[name] = []
            for cell in cells[1:]:
                total[name].append(cell.contents[0].strip())

    return data, meal_total, total

if __name__ == "__main__":

    args = sys.argv

    # check for username and password and optional number of days to get
    if len(args) != 2:
        print "Incorrect number of arguments"
        print "Argument pattern: username "
        exit(1)

    username = args[1]

    extract_data(username)     
         





