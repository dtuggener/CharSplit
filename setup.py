import setuptools


setuptools.setup(
    name = "charsplit",
    version = "0.1",
    author = "Don Tuggener",
    author_email = "don.tuggener@gmail.com",
    description = "Splitting compound german words into subwords.",
    description_long = "A tool for splitting german compound word into subwords, such as Autobahnraststätte --> Autobahn, Raststätte. Based on the thesis `Tuggener, Don (2016). Incremental Coreference Resolution for German. University of Zurich, Faculty of Arts.`",
    url = "https://github.com/dtuggener/CharSplit",
    packages=["charsplit"],
    include_package_data=True,
    scripts = ["charsplit/training.py"],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)