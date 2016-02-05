## -*- coding: utf-8 -*-
# Annonces

Offres d'emploi python pour le marché français

% for job in jobs:
* ${job.publication_datetime.strftime('%Y/%m/%d')} - [${job.title}](${h.get_job_url(job.id, job.title)} "${job.title}")
% endfor
