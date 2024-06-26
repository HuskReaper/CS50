document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
})

function compose_email() {
  const emails_view = document.querySelector('#emails-view')
  const compose_view = document.querySelector('#compose-view')
  const detailed_view = document.querySelector('#detailed-view')

  // Show compose view and hide other views
  emails_view.style.display = 'none';
  compose_view.style.display = 'block';
  detailed_view.style.display = 'none';

  // Clear out composition fields
  const recipients = document.querySelector('#compose-recipients')
  const subject = document.querySelector('#compose-subject')
  const body = document.querySelector('#compose-body')

  recipients.value = '';
  subject.value = '';
  body.value = '';

  document.querySelector('#compose-form').onsubmit = (event) => {
    event.preventDefault()
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients.value,
          subject: subject.value,
          body: body.value
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
    load_mailbox('sent');
  }
}

function load_mailbox(mailbox) {
  const emails_view = document.querySelector('#emails-view')
  const compose_view = document.querySelector('#compose-view')
  const detailed_view = document.querySelector('#detailed-view')

  // Show the mailbox and hide other views
  emails_view.style.display = 'block';
  compose_view.style.display = 'none';
  detailed_view.style.display = 'none';

  // Show the mailbox name
  emails_view.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // Fetch an array of all available emails.
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(element => {
      // Create a div to place info in & wrap div with an a element for functionalities.
      const div = document.createElement('div')
      const a = document.createElement('a')
      div.className = 'row'

      // Get info from element to display.
      const subject = element.subject
      const sender = element.sender
      const timestamp = element.timestamp

      // Wrap div in a and remove decorations.
      a.appendChild(div)
      a.href=''
      a.style.color = 'black'
      a.style.textDecoration = 'none'
      emails_view.appendChild(a)

      // If email was read, change div background to a light gray color.
      if (element.read) {
        div.style.backgroundColor = 'LightGray';
      }

      // When an email is clicked, show detailed_view and hide other views.
      a.addEventListener('click', (event) => {
        event.preventDefault()
        emails_view.style.display = 'none';
        compose_view.style.display = 'none';
        detailed_view.style.display = 'block';

        // Mark email as read.
        fetch(`/emails/${element.id}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
          })
        })

        // Fetch data from email.
        fetch(`/emails/${element.id}`)
        .then(response => response.json())
        .then(data => {
          // Update inner html of div to display emails information.
          detailed_view.innerHTML = 
          `
          <p>From: ${data.sender}</p>
          <p>To: ${data.recipients}</p>
          <p>Timestamp: ${data.timestamp}</p>
          <hr>
          <h1>${data.subject}</h1>
          <br>
          <h5>${data.body}</h5>
          <button id='archive_btn'>Archive</button>
          <button id='reply_btn'>Reply</button>
          `

          // Logical part of the "archive" function.
          if (data.archived) {
            archive_btn.innerHTML = 'Unarchive'
            btn = document.querySelector('#archive_btn')
            btn.addEventListener('click', () => {
              fetch(`/emails/${element.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                  archived: false
                })
              })
              load_mailbox('inbox');
            })
          } else {
            archive_btn.innerHTML = 'Archive'
            btn = document.querySelector('#archive_btn')
            btn.addEventListener('click', () => {
              fetch(`/emails/${element.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                  archived: true
                })
              })
              load_mailbox('inbox');
            })
          }
          // Logical part of the "reply" function.
          btna = document.querySelector('#reply_btn')
          btna.addEventListener('click', () => {
            compose_email() // Redirect to compose an email.
            let subject = data.subject // Get temp subject from data

            // Add Re: to subject if it is not already in there.
            document.querySelector('#compose-recipients').value = data.sender;
            if (subject.split(' ', 1)[0] != "Re:") {
              subject = "Re: " + data.subject
            }

            // Modify subject and body.
            document.querySelector('#compose-subject').value = `${subject}`;
            document.querySelector('#compose-body').value = `On ${data.timestamp}, ${data.sender} wrote: "${data.body}"`;
          })

        })
      })

      // Modify div contents.
      div.innerHTML = 
      `
        <div class='col'>${sender}</div>
        <div class='col-5'>${subject}</div>
        <div class='col'>${timestamp}</div>
      `
    });
  })
}