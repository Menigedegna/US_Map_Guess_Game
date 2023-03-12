import math
import turtle
import pandas as pd

POSITION_PRECISION = 50
FONT = ("Times New Roman", 10, "bold")


def write_state(location, state_name, turtle_name):
    """use turtle and location to display state_name on canvas"""
    turtle_name.goto(location)
    turtle_name.write(state_name, align="center", font=FONT)


def calculate_distance(position1, position2):
    """calculate distance between two points and return distance: float"""
    distance = math.sqrt((position1[0]-position2[0])**2 + (position1[1]-position2[1])**2)
    return distance


def get_closest_state(states_df, mouse_position):
    """return name of the closest state"""
    selected_states_positions = [[a, b] for a, b in zip(list(states_df.x), list(states_df.y))]
    distance_list = [calculate_distance(position1=state_position, position2=mouse_position)
                     for state_position in selected_states_positions]
    index_closest_state = distance_list.index(min(distance_list))
    selected_state_names = list(states_df.state)
    closest_state = selected_state_names[index_closest_state]
    return closest_state


def print_coordinate(x, y):
    """ check if user guesses state clicked on, and stores the state names correctly guessed"""
    global score, writing_turtle, states_guessed
    user_input = screen.textinput(title=f"{score}/50 Guess the state", prompt="What's another state name?")
    user_input = user_input.strip().title()

    '''if user's input is not exit'''
    if user_input != "Exit":
        '''get dataframe with closest states in POSITION_PRECISION radius of mouse click'''
        selected_x_states = data[data.x <= x+POSITION_PRECISION]
        selected_x_states = selected_x_states[selected_x_states.x >= x-POSITION_PRECISION]
        selected_y_states = selected_x_states[selected_x_states.y <= y+POSITION_PRECISION]
        selected_y_states = selected_y_states[selected_y_states.y >= y-POSITION_PRECISION]

        '''if user's input is among the closest states'''
        selected_state = list(selected_y_states.state)
        if user_input in selected_state:
            # calculate distance from mouse click to all closest states and get the closest state
            closest_state = get_closest_state(states_df=selected_y_states, mouse_position=[x, y])

            '''if user guessed that state'''
            if closest_state == user_input:
                score += 1
                selected_state = data[data.state == closest_state]
                closest_state_position = (int(selected_state.x), int(selected_state.y))
                write_state(location=closest_state_position, state_name=user_input, turtle_name=writing_turtle)
                states_guessed.append(user_input)

    else:
        '''if user's input is exit -> exit screen'''
        screen.bye()


if __name__ == "__main__":
    screen = turtle.Screen()
    screen.title("U.S. States Game")

    # set background to US map
    image = "blank_states_img.gif"
    screen.addshape(image)
    turtle.shape(image)

    # get states' coordinates
    data = pd.read_csv("50_states.csv")

    # create turtle to write state name with
    writing_turtle = turtle.Turtle(shape="square")
    writing_turtle.hideturtle()
    writing_turtle.penup()

    # keep track of score
    score = 0

    # keep track of guessed states
    states_guessed = []

    # start game
    turtle.onscreenclick(print_coordinate)
    turtle.mainloop()

    # saved states user missed to csv file
    missed_states = data[~data.state.isin(states_guessed)]
    missed_states.to_csv("Missed_states.csv")
