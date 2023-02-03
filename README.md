# AI-blogger

Using AI to create a self-sustained blog in seconds.

See how it works here: https://youtu.be/TlKTIwGa-S4

The AI-blogger project was originated by [Patrick Gerard](https://www.linkedin.com/in/patrick-gerard-konstanz/)
of [Contentbär](https://content-baer.de) with the objective of demonstrating the
capabilities of AI in content creation, specifically for the purpose of optimizing search engine results. The aim was to
create a case study that highlights the potential of AI in this field.

Introducing AI-blogger, a powerful command-line tool that harnesses the power of OpenAI API, WordPress, and Python to
revolutionize the way you create blog posts. Say goodbye to hours of writing, researching, and editing - AI-blogger
generates high-quality blog posts in mere seconds.

With its advanced AI capabilities, AI-blogger can understand and analyze the context of your topic, generating content
that is both informative and engaging. Whether you're looking to save time or just need inspiration, AI-blogger is the
perfect solution for anyone who wants to take their blogging to the next level.

Built on the popular WordPress platform, AI-blogger is easy to set up and use, with a user-friendly interface that makes
it a breeze to create and publish posts. And, with its Python integration, you can customize and extend the
functionality of AI-blogger to meet your unique needs.

So if you're looking for a faster, easier, and more effective way to create blog posts, look no further than AI-blogger.
Try it today and see how you can take your blogging to the next level with the power of AI.

## Setup WordPress

Custom CSS

```
        .faq-container {
    display: flex;
    flex-wrap: wrap;
    align-items: flex-start;
    width: 100%;
}

h3 {
    width: 100%;
    margin-bottom: 10px;
}

.faq-answer {
    width: 100%;
    padding: 10px;
    background-color: #f2f2f2;
    border-radius: 5px;
    margin-bottom: 20px;
}
```

Install WordPress and download the [JWT Auth Plugin from Useful Team](https://wordpress.org/plugins/jwt-auth/).
Also download [SEO REST API from Zippy](https://bn.wordpress.org/plugins/seo-rest-api/).

Edit the `.htaccess file` in the root directory of your WordPress installation and add the following line:

How to:

```
docker exec -it <container_name> bash
apt-get update
apt-get install vim
cd /var/www/html
vim .htaccess
```

add the following

```
RewriteEngine on
RewriteCond %{HTTP:Authorization} ^(.*)
RewriteRule ^(.*) - [E=HTTP_AUTHORIZATION:%1]
SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1
```

also change your `wp-config.php`

```
define('JWT_AUTH_SECRET_KEY', 'your-top-secret-key');
```

more information: https://github.com/usefulteam/jwt-auth

## Setup search console

Explained here: https://content-baer.de/google-search-console-api/

## Setup AI-blogger

fill the `config.ini` with your credentials

Run `make test` to check if everything is working

## Commands

to get an overview of commands use `python3 main.py -h`

```
Usage: cli.py [OPTIONS]

  Simple program that greets NAME for a total of COUNT times.

Options:
  --count INTEGER  Number of greetings.
  --name TEXT      The person to greet.
  --help           Show this message and exit.
```

## Example usage

`python3 cli.py "Das Spiel Leauge of Legends" --picture "Leauge of Legends" --faq --search_console`

This will create an article about "Das Spiel League of Legends", add a Picture from Unsplash, add FAQ and directly
sends the released post to the search console.

## How to contribute

1. Fork the repository
2. Clone the forked repository to your local machine
3. Make your changes and ensure that all tests are passing
4. Create a pull request to the original repository
5. The repository maintainer will review your changes and merge if all tests pass and the changes are deemed to be a
   positive contribution to the project.

Note: It is recommended that contributors run all tests before making a pull request to ensure the integrity of the
project.

*It would be nice if you start contributing by opening an issue for the feature you want to implement or the bug you
want to fix. This way we can discuss the implementation details before you start coding.*
*Some ideas are in the TODO.md*

## For people who want to use it

Change the config.ini to your needs and play around with it. Feel free to change the `promots and templates` and
show your results in case they are good.