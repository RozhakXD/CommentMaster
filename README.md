# CommentMaster
![CommentMaster Images](https://github.com/user-attachments/assets/eb333ed7-2276-4eea-8218-08a6fd3daede)

**CommentMaster** is a powerful Python tool designed to automatically comment on all Facebook posts within a specified group. Whether you want to comment with text, images, or both, CommentMaster handles it all effortlessly.

## Key Features
- **Customizable Delay**: Set a delay between comments to avoid getting flagged by Facebook, with a recommended minimum of 60 seconds.
- **Automated Comments**: Automatically comment on all posts within a specified Facebook group, saving you time and effort.
- **Image Support**: Attach images to your comments or opt for text-only comments, giving you flexibility in how you engage.
- **Random Comments**: Provide multiple comments, and CommentMaster will randomly select one for each post. Use commas to separate comments and `+` for line breaks.

## How It Works
- **Comment Delay**: Set a delay between comments to prevent being blocked. A delay of 60 seconds or more is recommended.
- **Group Link**: Provide the Facebook group link, and CommentMaster will target all posts in that group.
- **Image Path**: Specify the image file path or leave it blank for text-only comments.
- **Comment Text**: Enter your comments, separated by commas for randomization. Use `+` for line breaks.

## Installation
```
$ apt update -y && apt upgrade -y
$ pkg install git python-pip
$ git clone https://github.com/RozhakXD/CommentMaster.git
$ cd CommentMaster
$ pip install requests rich requests-toolbelt
$ python Run.py
```

## Support
If you find this tool helpful, consider supporting its development:

- [Trakteer](https://trakteer.id/rozhak_official/tip)
- [PayPal](https://paypal.me/rozhak9)

## Troubleshooting
- **Valid Cookies**: Ensure your cookies are valid and up-to-date to avoid login issues and maintain a stable connection with Facebook.
- **Correct Group Link**: Double-check that the Facebook group link is properly formatted. An incorrect link can prevent CommentMaster from targeting the right group.
- **Image File Path**: Verify that the image file path is correct if you're using an image. An incorrect path will result in failure to attach the image to your comments.
- **Adequate Delay**: Set the comment delay to at least 60 seconds. This helps to minimize the risk of your account being flagged or blocked by Facebook's automated systems.

## Screenshot
![FunPic_20240825](https://github.com/user-attachments/assets/787ca2ce-482c-4bfe-858a-d342b2a1c487)

## License
This project is licensed under the GNU General Public License. See the [LICENSE](https://github.com/RozhakXD/CommentMaster?tab=GPL-3.0-1-ov-file) file for more details.
