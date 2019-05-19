import matplotlib.pyplot as plt


def draw_single_point(xpnt, ypnt, title):
    # Draw a point at the location (3, 9) with size 1000
    # plt.scatter(xpnt, ypnt, s=100)
    plt.plot(xpnt, ypnt, 'ro', s=1000)

    # Set chart title.
    plt.title(title)

    # Set x axis label.
    plt.xlabel("x - axis", fontsize=10)

    # Set y axis label.
    plt.ylabel("y - axis", fontsize=10)

    # Set size of tick labels.
    plt.tick_params(axis='both', which='major', labelsize=9)

    plt.axis([0, xpnt + 50, ypnt + 50, 0])

    for i_x, i_y in zip(xpnt, ypnt):
        plt.text(i_x, i_y, '({}, {})'.format(i_x, i_y))

    # Display the plot in the matplotlib's viewer.
    plt.show()


# Draw multiple points.
def draw_multiple_points(x_number_list, y_number_list, title):
    # x axis value list.
    # x_number_list = [1, 4, 9, 16, 25]

    # y axis value list.
    # y_number_list = [1, 2, 3, 4, 5]

    # Draw point based on above x, y axis values.
    plt.scatter(x_number_list, y_number_list, s=100)

    # Set chart title.
    plt.title(title)

    for i_x, i_y in zip(x_number_list, y_number_list):
        plt.text(i_x, i_y, '({}, {})'.format(i_x, i_y))

    plt.axis([0, 800 + 50, 800 + 50, 0])

    # Set x, y label text.
    plt.xlabel("x - axis", fontsize=10)
    plt.ylabel("y - axis", fontsize=10)
    plt.show()
