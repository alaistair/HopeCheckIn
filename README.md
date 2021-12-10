# `client-hope`

[Open in Gitpod.io](https://gitpod.io/#https://github.com/DataBooth/client-hope)

[Hope Anglican](https://www.hopeanglicanchurch.org) Leppington: Automated check-in solution

## Background

Hope Anglican is a fast growing church in south west Sydney. With the coming completion of its building project they are looking to upgrade their check in system.

Hope currently runs three Sunday services: 9am, 10.45am, and 6pm. The two morning services have around 150 attendees each. Given the bigger capacity of the new building, the plan is to combine the 9am and 10.45am services. The new building is expected to be finished in November and the services will be combined in time for the Christmas service (God willing).

Hope asked us to help rethink the entire check-in process, which has suffered in the past from buggy systems and lack of scalability. Hope has a budget of $10,000 left from the building project to devote to building a proper check in solution.

Requirements (so far) include:
1) Ability to check in ~300 people within 15 minutes
2) Newcomer details captured
3) Physical nametags for each attendee
4) COVID check in automated

## Requirements discussion

1) Ability to check in ~300 people within 15 minutes

Service attendance is captured quite rigorously for both mission and pastoral care purposes. Currently for each morning service there are typically two volunteers from the Welcome team as well as one pastor (Andy Bootes) who greet attendees, check in people, and capture newcomer details as needed.

Attendance data is stored in Hope's CMS (Elvanto) and there are no plans to change this at this point. Given that large crowds typically show up one minute before service start, sometimes data is not captured correctly and the team will meet on Sunday afternoon to clean the data.

Any solution will need to maintain this data capture, while also have the ability to scale for future growth (NB: Hope has doubled in size every year since its inception, which is not a boast as the Leppington area is the fastest growing in the country). 

2) Newcomer details captured

Related to point 1), when newcomers arrive their contact details (phone number at minimum, email/physical address if possible) are captured for followup. With families, ages of children are noted so that they can be triaged into Hope Kids programs. Allergies are also noted if any.

3) Physical nametags for each attendee

The Hope welcome team learned a while back that, given the high number of new attendees at each service, physical nametags for everyone was best to encourage conversations among relative strangers and also remove the feeling of separation among newcomers.

The team recently moved away from handwriting nametags to a printer solution, with mixed results. The printer is liable to suffer issues during periods of high volume.

4) Automated data capture

Service attendance is captured for both mission and pastoral care purposes. Currently for each morning service there are typically two volunteers from the Welcome team as well as one pastor (Andy Bootes) who greet attendees, check in people, and capture newcomer details as needed.

Attendance data is stored in Hope's CMS (Elvanto) and there are no plans to change this at this point. Given that large crowds typically show up one minute before service start, sometimes data is not captured correctly and the team will meet on Sunday afternoon to clean the data.

Any solution will need to maintain this data capture, while also have the ability to scale for future growth (NB: Hope has doubled in size every year since its inception).



## Solution architecture

One overarching requirement is that there will still be a human element in any solution. Having a fully automated solution, while being more streamlined, may also reduce the time that greeters have with newcomers and hence may reduce the opportunity to make connections.

Moreover, although there are benefits to simply providing a QR code for attendees to scan and self check in with their phones, there is likely to be a reduction in accuracy of the data captured. Latecomers may claim to check in after the service and forget. Parents may also not check in if they are wrangling young children.

Hope is quite rigorous in its maintainance and usage of attendance data. Eg people who have not shown up for 2-3 weeks consecutively are followed up by the mission staff. Newcomers who have attended regularly are invited to the pastor's house for a monthly Welcome lunch. Members are also identified for mission/serving roles given their maturity level, which attendance plays a part. Etc.

## Report on Elvanto/DYMO POC (28 Nov 2021, 6pm service)

### Setup

DataBooth (Alaistair & Michael) set up a MacBook connected to a DYMO LabelWriter 450 and DYMO LabelWriter 450 Turbo. We also had two iPads set up for self check-ins. The iPads were mapped to their own printer, and each printer had a dedicated print station set up in Elvanto. Two people from the Welcome team used the iPads to check existing contacts in. We checked in all 80 attendees to the 6pm service this way. 14 newcomers were also checked in by Alaistair via the MacBook, with details captured in Elvanto.
 
### Observations

This system worked for the most part. There are ongoing problems with the DYMOs, which were resolved by checking people back out, and then checking them in again to put them back in the printer queue. This created a bit of a line just after 6pm. We feel that it is unlikely that, given the inherent limitations of these printers, this system would work well and sustainably for the morning services.

### Recommendations

While not our preferred option, we could test this on the morning services. It would need to be scaled up for it to possibly work. Here are some options to consider:

#### 1. Scale up existing Elvanto/DYMO system
Given the 9am service is about double the size of 6pm, we’d probably have to double (at least) the existing setup if we maintained what we have. Ie another two DYMO LabelWriters, and another laptop. I think with this method we should also have iPads for the Welcome team (rather than allow people to check themselves in) because of the known issues with the DYMO printers.

This is probably the easiest experiment to trial as we already have part of the solution set up. Also the check in data and new visitor data are automatically captured in Elvanto. The main downside is that the DYMO printers are unreliable and those two models are the only ones Elvanto supports.

#### 2. New solution
We think we can create a light-weight online app that allows people to self check in via QR code link and then also prints out a name tag. What we can do is have a list of people that can be searched via last name (similar to Elvanto) that visitors can access and then print out their own labels.

If we create something ourselves we can also set up a different print option ([Brother QL Label Printers](https://www.brother.com.au/en/products/all-labellers/labellers) look like a good option which can be trialled for [less than $90](https://www.inkstation.com.au/brother-ql700-label-printer-machine-p-16283.html). These printers have the [`brother-ql`](https://pypi.org/project/brother-ql/) Python package for easy software control and integration.

The main issue here is that the check in data will be saved outside of Elvanto (eg in a CSV file) and will have to be manually entered/reconciled (as an interim step) in after the service.

#### 3. Manual backup 

In the case that access to data (via WiFi or mobile network) or the power is out, it is good to have a simply documented and well understood failover system.
TODO: Alaistair to complete.

#### 4. Reusable DIY nametags

A note that we also demonstrated a couple of DIY felt nametags last Sunday night. TODO: Alaistair to comment.
