import csv
import os
import argparse
import matplotlib.pyplot as plt


def read_training_log(filepath):
    epochs = []
    collected = []
    steps = []
    reward_total = []
    best_score = []
    snake_length = []
    epsilon = []
    levels = []

    with open(filepath, "r", newline="") as f:
        reader = csv.DictReader(f)

        has_level = "level" in reader.fieldnames

        for row in reader:
            epochs.append(int(row["epochs"]))
            collected.append(float(row["collected"]))
            steps.append(float(row["steps"]))
            reward_total.append(float(row["reward_total"]))
            best_score.append(float(row["best_score"]))
            snake_length.append(float(row["snake_length"]))
            epsilon.append(float(row["epsilon"]))

            if has_level:
                levels.append(int(row["level"]))

    return epochs, collected, steps, reward_total, best_score, snake_length, epsilon, levels


def moving_average(values, window):
    if window <= 1:
        return values

    result = []
    for i in range(len(values)):
        start = max(0, i - window + 1)
        avg = sum(values[start:i + 1]) / len(values[start:i + 1])
        result.append(avg)

    return result


def add_level_lines(epochs, levels):
    if len(levels) == 0:
        return

    previous_level = levels[0]

    for i in range(1, len(levels)):
        if levels[i] != previous_level:
            plt.axvline(x=epochs[i], linestyle="--")
            plt.text(epochs[i], plt.ylim()[1], f"Level {levels[i]}", rotation=90, verticalalignment="top")
            previous_level = levels[i]


def save_plot(x, y, title, xlabel, ylabel, filename, output_dir, y_ma=None, levels=None, show=False):
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, label=ylabel)

    if y_ma is not None:
        plt.plot(x, y_ma, label="Moving Average")

    if levels is not None and len(levels) > 0:
        add_level_lines(x, levels)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    path = os.path.join(output_dir, filename)
    plt.savefig(path)

    if show:
        plt.show()

    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default="training_log.csv", help="CSV file")
    parser.add_argument("--window", type=int, default=50, help="Moving average window")
    parser.add_argument("--show", action="store_true", help="Show plots")
    args = parser.parse_args()

    csv_file = args.file
    window = args.window
    show_plots = args.show

    if not os.path.exists(csv_file):
        print("Fisierul nu exista:", csv_file)
        return

    output_dir = "plots"
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(csv_file))[0]

    epochs, collected, steps, reward_total, best_score, snake_length, epsilon, levels = read_training_log(csv_file)

    collected_ma = moving_average(collected, window)
    reward_ma = moving_average(reward_total, window)
    steps_ma = moving_average(steps, window)
    snake_length_ma = moving_average(snake_length, window)

    save_plot(
        epochs,
        collected,
        "Collected per Episode",
        "Epoch",
        "Collected",
        f"{base_name}_collected.png",
        output_dir,
        collected_ma,
        levels,
        show_plots
    )

    save_plot(
        epochs,
        reward_total,
        "Reward per Episode",
        "Epoch",
        "Reward",
        f"{base_name}_reward.png",
        output_dir,
        reward_ma,
        levels,
        show_plots
    )

    save_plot(
        epochs,
        steps,
        "Steps per Episode",
        "Epoch",
        "Steps",
        f"{base_name}_steps.png",
        output_dir,
        steps_ma,
        levels,
        show_plots
    )

    save_plot(
        epochs,
        best_score,
        "Best Score Over Time",
        "Epoch",
        "Best Score",
        f"{base_name}_best_score.png",
        output_dir,
        None,
        levels,
        show_plots
    )

    save_plot(
        epochs,
        snake_length,
        "Snake Length per Episode",
        "Epoch",
        "Snake Length",
        f"{base_name}_snake_length.png",
        output_dir,
        snake_length_ma,
        levels,
        show_plots
    )

    save_plot(
        epochs,
        epsilon,
        "Epsilon Decay",
        "Epoch",
        "Epsilon",
        f"{base_name}_epsilon.png",
        output_dir,
        None,
        levels,
        show_plots
    )

    print("Graficele au fost salvate in folderul:", output_dir)


if __name__ == "__main__":
    main()