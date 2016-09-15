## -*- coding: utf-8 -*-
# Annonces

Offres d'emploi python pour le marché français

% if new_job:
* ${new_job.publication_datetime.strftime('%Y/%m/%d')} - [${new_job.title}](${get_job_url(new_job.id, new_job.title, absolute=True)} "${new_job.title}")
% endif
% for old_job in old_jobs:
${old_job}
% endfor
